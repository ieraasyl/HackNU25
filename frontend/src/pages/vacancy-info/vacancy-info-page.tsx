import {
  Container,
  Stack,
  Text,
  Badge,
  Group,
  Button,
  Card,
  Box,
  ActionIcon,
  Divider,
} from "@mantine/core";
import {
  ArrowLeft,
  MapPin,
  Clock,
  DollarSign,
  Building2,
  Bookmark,
  Share2,
} from "lucide-react";
import { mockJobs } from "../../features/vacancies/lib/mock-data";
import { useNavigate } from "react-router";

interface VacancyInfoPageProps {
  jobId?: string;
}

export function VacancyInfoPage({ jobId = "1" }: VacancyInfoPageProps) {
  const job = mockJobs.find((job) => job.id === jobId) || mockJobs[0];
  const navigate = useNavigate();

  const handleBack = () => {
    navigate("/");
  };

  if (!job) {
    return (
      <Container style={{ minHeight: "100vh" }}>
        <Stack align="center" justify="center" style={{ minHeight: "50vh" }}>
          <Text size="xl" c="dimmed">
            Job not found
          </Text>
          <Button onClick={handleBack}>Back to Jobs</Button>
        </Stack>
      </Container>
    );
  }

  return (
    <Container
      size="lg"
      style={{ minHeight: "100vh", paddingTop: "2rem", paddingBottom: "2rem" }}
    >
      <Stack gap="xl">
        {/* Header with back button */}
        <Group>
          <ActionIcon variant="subtle" size="lg" onClick={handleBack}>
            <ArrowLeft size={20} />
          </ActionIcon>
          <Text size="sm" c="dimmed">
            Back to Jobs
          </Text>
        </Group>

        {/* Job Header Card */}
        <Card shadow="sm" padding="xl" radius="md" withBorder>
          <Stack gap="md">
            <Group justify="space-between" align="flex-start">
              <Stack gap="xs" style={{ flex: 1 }}>
                <Text size="xl" fw={700} c="#18191c">
                  {job.title}
                </Text>
                <Group gap="md">
                  <Group gap="xs">
                    <Building2 size={16} color="#767f8c" />
                    <Text size="md" fw={500} c="#0ba02c">
                      {job.company}
                    </Text>
                  </Group>
                  <Group gap="xs">
                    <MapPin size={16} color="#767f8c" />
                    <Text size="sm" c="#767f8c">
                      {job.location}
                    </Text>
                  </Group>
                </Group>
              </Stack>

              <Group gap="xs">
                <ActionIcon variant="light" color="gray" size="lg">
                  <Bookmark size={20} />
                </ActionIcon>
                <ActionIcon variant="light" color="gray" size="lg">
                  <Share2 size={20} />
                </ActionIcon>
              </Group>
            </Group>

            <Group gap="md">
              <Badge
                color="green"
                variant="light"
                size="md"
                styles={{
                  root: {
                    backgroundColor: "#e7f6ea",
                    color: "#0ba02c",
                    textTransform: "uppercase",
                    fontWeight: 600,
                  },
                }}
              >
                {job.type}
              </Badge>

              <Group gap="xs">
                <DollarSign size={16} color="#767f8c" />
                <Text size="sm" fw={500}>
                  {job.salary}
                </Text>
              </Group>

              <Group gap="xs">
                <Clock size={16} color="#767f8c" />
                <Text size="sm" c="#767f8c">
                  Posted {job.postedDate}
                </Text>
              </Group>
            </Group>

            <Group justify="space-between" mt="md">
              <Button
                size="lg"
                radius="md"
                style={{ flex: 1, maxWidth: "200px" }}
              >
                Apply Now
              </Button>
              <Text size="sm" c="#767f8c">
                {job.experience} experience required
              </Text>
            </Group>
          </Stack>
        </Card>

        {/* Main Content Grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "2fr 1fr",
            gap: "2rem",
            alignItems: "start",
          }}
        >
          {/* Left Column - Main Content */}
          <div
            style={{
              display: "grid",
              gap: "1.5rem",
            }}
          >
            {/* Job Description Card */}
            <Card shadow="sm" padding="xl" radius="md" withBorder>
              <Stack gap="md">
                <Text size="lg" fw={600} c="#18191c">
                  Job Description
                </Text>
                <Text size="sm" c="#4f4f4f" style={{ lineHeight: 1.6 }}>
                  {job.description}
                </Text>
              </Stack>
            </Card>

            {/* Requirements Card */}
            <Card shadow="sm" padding="xl" radius="md" withBorder>
              <Stack gap="md">
                <Text size="lg" fw={600} c="#18191c">
                  Requirements
                </Text>
                <div
                  style={{
                    display: "grid",
                    gap: "0.5rem",
                  }}
                >
                  {job.requirements.map((requirement, index) => (
                    <Group key={index} gap="xs" align="flex-start">
                      <Box
                        style={{
                          width: 6,
                          height: 6,
                          backgroundColor: "#0ba02c",
                          borderRadius: "50%",
                          marginTop: 8,
                        }}
                      />
                      <Text size="sm" c="#4f4f4f" style={{ lineHeight: 1.6 }}>
                        {requirement}
                      </Text>
                    </Group>
                  ))}
                </div>
              </Stack>
            </Card>
          </div>

          {/* Right Column - Sidebar */}
          <div
            style={{
              display: "grid",
              gap: "1rem",
              gridTemplateRows: "max-content",
              position: "sticky",
              top: "2rem",
            }}
          >
            {/* Quick Apply Card */}
            <Card shadow="sm" padding="lg" radius="md" withBorder>
              <div
                style={{
                  display: "grid",
                  gap: "1rem",
                }}
              >
                <Text size="md" fw={600} c="#18191c">
                  Quick Apply
                </Text>
                <Button fullWidth size="md" radius="md">
                  Apply Now
                </Button>
                <Divider />

                {/* Job Details Grid */}
                <div
                  style={{
                    display: "grid",
                    gap: "0.75rem",
                  }}
                >
                  <div style={{ display: "grid", gap: "0.25rem" }}>
                    <Text size="sm" fw={500} c="#18191c">
                      Job Type
                    </Text>
                    <Text size="sm" c="#767f8c">
                      {job.type}
                    </Text>
                  </div>

                  <div style={{ display: "grid", gap: "0.25rem" }}>
                    <Text size="sm" fw={500} c="#18191c">
                      Experience
                    </Text>
                    <Text size="sm" c="#767f8c">
                      {job.experience}
                    </Text>
                  </div>

                  <div style={{ display: "grid", gap: "0.25rem" }}>
                    <Text size="sm" fw={500} c="#18191c">
                      Salary
                    </Text>
                    <Text size="sm" c="#767f8c">
                      {job.salary}
                    </Text>
                  </div>

                  <div style={{ display: "grid", gap: "0.25rem" }}>
                    <Text size="sm" fw={500} c="#18191c">
                      Location
                    </Text>
                    <Text size="sm" c="#767f8c">
                      {job.location}
                    </Text>
                  </div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </Stack>
    </Container>
  );
}
