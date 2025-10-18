import { Container } from "@mantine/core";
import { Header } from "../../features/vacancies/components/header";
import { mockJobs } from "../../features/vacancies/lib/mock-data";
import { JobCard } from "../../features/vacancies/components/job-card";
import { useNavigate } from "react-router";

export default function VacanciesPage() {
  const navigate = useNavigate();

  return (
    <Container style={{ minHeight: "100vh" }}>
      <div className="min-h-screen bg-background">
        <Header />

        <main className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <div className="mb-12 text-center"></div>

          <div className="mb-8 flex items-center justify-between">
            <h2 className="text-2xl font-semibold text-foreground">
              Latest Positions
            </h2>
            <p className="text-muted-foreground">
              {mockJobs.length} open positions
            </p>
          </div>

          <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 ">
            {mockJobs.map((job) => (
              <JobCard
                key={job.id}
                title={job.title}
                company={job.company}
                location={job.location}
                employmentType={job.type}
                salary={job.salary}
                onBookmark={() => console.log(`Bookmarked ${job.title}`)}
                onClick={() => navigate(`/vacancy/${job.id}`)}
              />
            ))}
          </div>
        </main>
      </div>
    </Container>
  );
}
