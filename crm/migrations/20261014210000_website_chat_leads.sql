-- Website chat leads for devindesaulniers.ca
-- Supabase project: gwmfrxnoxoknzfuzktqi
--
-- Run this once in the Supabase SQL editor. It has not been applied.
-- Do not run it from the website, and do not commit a service-role key.
--
-- What visitors can do after this runs:
--   call submit_website_chat_lead (add one lead)
-- What visitors cannot do:
--   read, list, update, or delete leads
--
-- A signed-in Desk user can read the inbox table website_chat_leads.
-- The function also tries to add a contact, a lead, a note, and a
-- "Call now" task in Desk. If those tables differ, the inbox row is
-- still kept and desk_status says why the Desk copy failed.

create schema if not exists website_chat_private;

revoke all on schema website_chat_private from public;
revoke all on schema website_chat_private from anon;
revoke all on schema website_chat_private from authenticated;

create table if not exists public.website_chat_leads (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  intent text not null,
  area text not null,
  budget text not null,
  timeline text not null,
  name text not null,
  phone text,
  email text,
  page_url text,
  desk_status text,
  constraint website_chat_leads_intent check (intent in ('buy', 'sell', 'rent')),
  constraint website_chat_leads_contact check (
    (phone is not null and length(btrim(phone)) > 0)
    or (email is not null and length(btrim(email)) > 0)
  )
);

comment on table public.website_chat_leads is
  'Inbox for the public website chat. Anonymous visitors cannot read this table.';

create index if not exists website_chat_leads_created_at_idx
  on public.website_chat_leads (created_at desc);

alter table public.website_chat_leads enable row level security;
alter table public.website_chat_leads force row level security;

revoke all on table public.website_chat_leads from public;
revoke all on table public.website_chat_leads from anon;
revoke all on table public.website_chat_leads from authenticated;
grant select on table public.website_chat_leads to authenticated;

drop policy if exists website_chat_leads_read_signed_in on public.website_chat_leads;
create policy website_chat_leads_read_signed_in
  on public.website_chat_leads
  for select
  to authenticated
  using (true);

-- Writes a row using only columns that exist. Not callable by visitors.
create or replace function website_chat_private.write_row(p_table text, p_data jsonb)
returns text
language plpgsql
security definer
set search_path = public
as $$
declare
  rec record;
  col_list text := '';
  val_list text := '';
  expr text;
  new_id text;
begin
  if p_table not in ('persons', 'leads', 'notes', 'activities') then
    raise exception 'Not allowed';
  end if;
  if to_regclass('public.' || p_table) is null then
    return null;
  end if;

  for rec in
    select column_name, udt_name
    from information_schema.columns
    where table_schema = 'public'
      and table_name = p_table
  loop
    if not (p_data ? rec.column_name) then
      continue;
    end if;
    if jsonb_typeof(p_data -> rec.column_name) is null
       or jsonb_typeof(p_data -> rec.column_name) = 'null' then
      continue;
    end if;

    if rec.udt_name in ('jsonb', 'json') then
      expr := format('%L::%s', (p_data -> rec.column_name)::text, rec.udt_name);
    elsif rec.udt_name in ('_text', '_varchar') then
      expr := format(
        'coalesce((select array_agg(x) from jsonb_array_elements_text(%L::jsonb) as t(x)), array[]::text[])',
        (p_data -> rec.column_name)::text
      );
    elsif rec.udt_name = 'bool' then
      expr := format('%L::boolean', p_data ->> rec.column_name);
    elsif rec.udt_name = 'uuid' then
      expr := format('%L::uuid', p_data ->> rec.column_name);
    elsif rec.udt_name = 'date' then
      expr := format('%L::date', p_data ->> rec.column_name);
    elsif rec.udt_name = 'timestamp' then
      expr := format('%L::timestamp', p_data ->> rec.column_name);
    elsif rec.udt_name = 'timestamptz' then
      expr := format('%L::timestamptz', p_data ->> rec.column_name);
    elsif rec.udt_name = 'int2' then
      expr := format('%L::smallint', p_data ->> rec.column_name);
    elsif rec.udt_name = 'int4' then
      expr := format('%L::integer', p_data ->> rec.column_name);
    elsif rec.udt_name = 'int8' then
      expr := format('%L::bigint', p_data ->> rec.column_name);
    elsif rec.udt_name = 'float4' then
      expr := format('%L::real', p_data ->> rec.column_name);
    elsif rec.udt_name = 'float8' then
      expr := format('%L::double precision', p_data ->> rec.column_name);
    elsif rec.udt_name = 'numeric' then
      expr := format('%L::numeric', p_data ->> rec.column_name);
    else
      expr := format('%L', p_data ->> rec.column_name);
    end if;

    col_list := col_list || format('%I, ', rec.column_name);
    val_list := val_list || expr || ', ';
  end loop;

  if col_list = '' then
    raise exception 'Nothing to save';
  end if;

  col_list := regexp_replace(col_list, ', $', '');
  val_list := regexp_replace(val_list, ', $', '');

  execute format(
    'insert into public.%I (%s) values (%s) returning id::text',
    p_table,
    col_list,
    val_list
  )
  into new_id;

  return new_id;
end;
$$;

revoke all on function website_chat_private.write_row(text, jsonb) from public;
revoke all on function website_chat_private.write_row(text, jsonb) from anon;
revoke all on function website_chat_private.write_row(text, jsonb) from authenticated;

create or replace function public.submit_website_chat_lead(
  p_intent text,
  p_area text,
  p_budget text,
  p_timeline text,
  p_name text,
  p_phone text default null,
  p_email text default null,
  p_page_url text default null,
  p_company text default null
)
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  v_intent text;
  v_area text;
  v_budget text;
  v_timeline text;
  v_name text;
  v_phone text;
  v_email text;
  v_page text;
  v_first text;
  v_last text;
  v_looking text;
  v_lead_type text;
  v_title text;
  v_note text;
  v_inbox_id uuid;
  v_person_id text;
  v_lead_id text;
  v_status text := 'saved';
  v_due text;
begin
  -- Honeypot. Filled in by bots. Act like it worked and save nothing.
  if coalesce(btrim(p_company), '') <> '' then
    return;
  end if;

  v_intent := lower(btrim(coalesce(p_intent, '')));
  v_area := left(btrim(coalesce(p_area, '')), 80);
  v_budget := left(btrim(coalesce(p_budget, '')), 80);
  v_timeline := left(btrim(coalesce(p_timeline, '')), 80);
  v_name := left(regexp_replace(btrim(coalesce(p_name, '')), '\s+', ' ', 'g'), 80);
  v_phone := nullif(left(btrim(coalesce(p_phone, '')), 40), '');
  v_email := nullif(lower(left(btrim(coalesce(p_email, '')), 160)), '');
  v_page := nullif(left(btrim(coalesce(p_page_url, '')), 300), '');

  if v_intent not in ('buy', 'sell', 'rent') then
    raise exception 'Please choose buy, sell, or rent.' using errcode = '22023';
  end if;
  if v_area = '' or v_budget = '' or v_timeline = '' or length(v_name) < 2 then
    raise exception 'Please answer each question.' using errcode = '22023';
  end if;
  if v_name ~ '[[:cntrl:]<>]' or v_area ~ '[[:cntrl:]<>]' then
    raise exception 'Please check what you typed.' using errcode = '22023';
  end if;
  if v_phone is null and v_email is null then
    raise exception 'Please add a phone number or an email.' using errcode = '22023';
  end if;
  if v_phone is not null and length(regexp_replace(v_phone, '\D', '', 'g')) < 7 then
    raise exception 'Please check the phone number.' using errcode = '22023';
  end if;
  if v_email is not null and v_email !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' then
    raise exception 'Please check the email address.' using errcode = '22023';
  end if;
  if v_page is not null and v_page !~ '^https?://' then
    v_page := null;
  end if;

  insert into public.website_chat_leads (
    intent, area, budget, timeline, name, phone, email, page_url
  ) values (
    v_intent, v_area, v_budget, v_timeline, v_name, v_phone, v_email, v_page
  )
  returning id into v_inbox_id;

  v_first := split_part(v_name, ' ', 1);
  v_last := nullif(btrim(substr(v_name, length(v_first) + 1)), '');
  v_looking := case v_intent
    when 'buy' then 'Buy a home'
    when 'sell' then 'Sell a home'
    else 'Rent a home'
  end;
  v_lead_type := case v_intent
    when 'buy' then 'buyer'
    when 'sell' then 'seller'
    else 'tenant'
  end;
  v_title := left(v_name || ' - ' || v_looking || ' (' || v_area || ')', 180);
  v_note := 'Website chat' || E'\n'
    || 'Looking to: ' || v_looking || E'\n'
    || 'Area: ' || v_area || E'\n'
    || 'Budget: ' || v_budget || E'\n'
    || 'Timeline: ' || v_timeline || E'\n'
    || 'Phone: ' || coalesce(v_phone, '') || E'\n'
    || 'Email: ' || coalesce(v_email, '') || E'\n'
    || 'Page: ' || coalesce(v_page, '');
  v_due := to_char((timezone('America/Vancouver', now()))::date, 'YYYY-MM-DD');

  begin
    v_person_id := website_chat_private.write_row('persons', jsonb_strip_nulls(jsonb_build_object(
      'name', v_name,
      'first_name', nullif(v_first, ''),
      'last_name', v_last,
      'emails', case
        when v_email is null then '[]'::jsonb
        else jsonb_build_array(jsonb_build_object('value', v_email, 'label', 'home', 'primary', true))
      end,
      'phones', case
        when v_phone is null then '[]'::jsonb
        else jsonb_build_array(jsonb_build_object('value', v_phone, 'label', 'mobile', 'primary', true))
      end,
      'label', 'warm',
      'deleted_in_pipedrive', false
    )));

    if v_person_id is null then
      v_status := 'Saved in the inbox. Desk contacts table was not found.';
    else
      v_lead_id := website_chat_private.write_row('leads', jsonb_strip_nulls(jsonb_build_object(
        'title', v_title,
        'person_id', v_person_id,
        'labels', jsonb_build_array('warm'),
        'lead_type', v_lead_type,
        'value_currency', 'CAD',
        'is_archived', false,
        'source', 'web_chat',
        'deleted_in_pipedrive', false
      )));

      if v_lead_id is null then
        v_status := 'Saved the contact. Desk leads table was not found.';
      else
        begin
          perform website_chat_private.write_row('notes', jsonb_build_object(
            'person_id', v_person_id,
            'content', v_note,
            'pinned', false,
            'deleted_in_pipedrive', false
          ));
        exception when others then
          null;
        end;

        begin
          perform website_chat_private.write_row('activities', jsonb_build_object(
            'subject', 'Call now',
            'type', 'call',
            'due_date', v_due,
            'priority', 'high',
            'person_id', v_person_id,
            'lead_id', v_lead_id,
            'done', false,
            'deleted_in_pipedrive', false
          ));
        exception when others then
          null;
        end;
      end if;
    end if;
  exception when others then
    v_status := left('Saved in the inbox. Desk copy failed: ' || sqlerrm, 300);
  end;

  update public.website_chat_leads
     set desk_status = v_status
   where id = v_inbox_id;
end;
$$;

comment on function public.submit_website_chat_lead(text, text, text, text, text, text, text, text, text) is
  'Insert-only path for the website chat. Anonymous visitors can add a lead. They cannot read leads.';

revoke all on function public.submit_website_chat_lead(text, text, text, text, text, text, text, text, text) from public;
revoke all on function public.submit_website_chat_lead(text, text, text, text, text, text, text, text, text) from anon;
revoke all on function public.submit_website_chat_lead(text, text, text, text, text, text, text, text, text) from authenticated;
grant execute on function public.submit_website_chat_lead(text, text, text, text, text, text, text, text, text) to anon;
grant execute on function public.submit_website_chat_lead(text, text, text, text, text, text, text, text, text) to authenticated;
