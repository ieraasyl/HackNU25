export interface Job {
  id: string;
  title: string;
  description: string;
  company: string;
  location: string;
  salary_min: string;
  salary_max: string;
  employment_type: string;
  requirements: Record<string, any>;
  created_at: string;
  updated_at: string;
}
