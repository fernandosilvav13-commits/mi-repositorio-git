-- Tabla: templates (plantillas de extracción)
create table if not exists templates (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  description text default '',
  columns jsonb not null default '[]',
  created_by uuid references auth.users(id),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Tabla: rules (reglas de negocio)
create table if not exists rules (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  description text default '',
  conditions jsonb not null default '[]',
  action jsonb not null,
  enabled boolean default true,
  created_by uuid references auth.users(id),
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

-- Tabla: extraction_results (resultados de extracción)
create table if not exists extraction_results (
  id uuid primary key default gen_random_uuid(),
  template_id uuid references templates(id) on delete cascade,
  filename text not null,
  status text not null default 'ok',
  data jsonb not null default '{}',
  error text,
  created_by uuid references auth.users(id),
  created_at timestamptz default now()
);

-- Row Level Security
alter table templates enable row level security;
alter table rules enable row level security;
alter table extraction_results enable row level security;

-- Políticas: cada usuario ve solo sus datos
create policy "Users can view own templates"
  on templates for select
  using (auth.uid() = created_by);

create policy "Users can insert own templates"
  on templates for insert
  with check (auth.uid() = created_by);

create policy "Users can update own templates"
  on templates for update
  using (auth.uid() = created_by);

create policy "Users can delete own templates"
  on templates for delete
  using (auth.uid() = created_by);

create policy "Users can view own rules"
  on rules for select
  using (auth.uid() = created_by);

create policy "Users can insert own rules"
  on rules for insert
  with check (auth.uid() = created_by);

create policy "Users can update own rules"
  on rules for update
  using (auth.uid() = created_by);

create policy "Users can delete own rules"
  on rules for delete
  using (auth.uid() = created_by);

create policy "Users can view own results"
  on extraction_results for select
  using (auth.uid() = created_by);

create policy "Users can insert own results"
  on extraction_results for insert
  with check (auth.uid() = created_by);

-- Trigger para updated_at
create or replace function update_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger update_templates_updated_at
  before update on templates
  for each row execute function update_updated_at();

create trigger update_rules_updated_at
  before update on rules
  for each row execute function update_updated_at();

-- Tabla: crossref_files (archivos de cruce de datos)
create table if not exists crossref_files (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  file_type text not null,
  columns jsonb not null default '[]',
  data jsonb not null default '[]',
  row_count int default 0,
  created_by uuid references auth.users(id),
  created_at timestamptz default now()
);

alter table crossref_files enable row level security;

create policy "Users can view own crossref files"
  on crossref_files for select
  using (auth.uid() = created_by);

create policy "Users can insert own crossref files"
  on crossref_files for insert
  with check (auth.uid() = created_by);

create policy "Users can delete own crossref files"
  on crossref_files for delete
  using (auth.uid() = created_by);

-- Índices
create index if not exists idx_templates_created_by on templates(created_by);
create index if not exists idx_rules_created_by on rules(created_by);
create index if not exists idx_extraction_results_template on extraction_results(template_id);
create index if not exists idx_crossref_files_created_by on crossref_files(created_by);

-- Columna de estado para tracking de matching
alter table crossref_files
  add column if not exists status text not null default 'unmatched';

-- Índice para filtrar por estado (Phase 03)
create index if not exists idx_crossref_files_status on crossref_files(status);
