export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  type: string;
  salary: string;
  experience: string;
  postedDate: string;
  description: string;
  responsibilities: string[];
  requirements: string[];
  benefits?: string[];
}

export const mockJobs: Job[] = [
  {
    id: "1",
    title: "Senior Frontend Engineer",
    company: "TechVision Inc",
    location: "San Francisco, CA",
    type: "Full-time",
    salary: "$140k - $180k",
    experience: "5+ years",
    postedDate: "2 days ago",
    description:
      "We are looking for an experienced Frontend Engineer to join our growing team. You will be responsible for building and maintaining our web applications using modern technologies.",
    responsibilities: [
      "Design and implement responsive web applications using React and Next.js",
      "Collaborate with designers and backend engineers to deliver high-quality features",
      "Optimize application performance and ensure cross-browser compatibility",
      "Mentor junior developers and contribute to code reviews",
      "Participate in architectural decisions and technical planning",
    ],
    requirements: [
      "5+ years of experience with JavaScript/TypeScript",
      "Strong proficiency in React, Next.js, and modern CSS",
      "Experience with state management libraries (Redux, Zustand, etc.)",
      "Understanding of web performance optimization techniques",
      "Excellent communication and collaboration skills",
    ],
    benefits: [
      "Competitive salary and equity package",
      "Comprehensive health, dental, and vision insurance",
      "Flexible work schedule and remote options",
      "401(k) matching",
      "Professional development budget",
    ],
  },
  {
    id: "2",
    title: "Full Stack Developer",
    company: "DataFlow Systems",
    location: "New York, NY",
    type: "Full-time",
    salary: "$120k - $160k",
    experience: "3+ years",
    postedDate: "1 week ago",
    description:
      "Join our team as a Full Stack Developer and work on cutting-edge projects that impact millions of users. We value innovation, collaboration, and continuous learning.",
    responsibilities: [
      "Develop and maintain both frontend and backend components",
      "Build RESTful APIs and integrate with third-party services",
      "Write clean, maintainable, and well-tested code",
      "Participate in agile development processes",
      "Troubleshoot and debug production issues",
    ],
    requirements: [
      "3+ years of full stack development experience",
      "Proficiency in Node.js, React, and SQL databases",
      "Experience with cloud platforms (AWS, GCP, or Azure)",
      "Strong understanding of software design patterns",
      "Bachelor's degree in Computer Science or related field",
    ],
    benefits: [
      "Competitive compensation package",
      "Health and wellness benefits",
      "Unlimited PTO",
      "Stock options",
      "Learning and development opportunities",
    ],
  },
  {
    id: "3",
    title: "DevOps Engineer",
    company: "CloudScale Solutions",
    location: "Austin, TX",
    type: "Full-time",
    salary: "$130k - $170k",
    experience: "4+ years",
    postedDate: "3 days ago",
    description:
      "We are seeking a talented DevOps Engineer to help us build and maintain our cloud infrastructure. You will work with cutting-edge technologies and help shape our deployment processes.",
    responsibilities: [
      "Design and implement CI/CD pipelines",
      "Manage and optimize cloud infrastructure on AWS",
      "Implement monitoring and alerting solutions",
      "Automate deployment and scaling processes",
      "Ensure security best practices across all systems",
    ],
    requirements: [
      "4+ years of DevOps or Site Reliability Engineering experience",
      "Strong knowledge of AWS services and infrastructure as code",
      "Experience with Docker, Kubernetes, and container orchestration",
      "Proficiency in scripting languages (Python, Bash, etc.)",
      "Understanding of networking and security principles",
    ],
    benefits: [
      "Competitive salary and bonuses",
      "Comprehensive benefits package",
      "Remote-first culture",
      "Home office stipend",
      "Annual team retreats",
    ],
  },
  {
    id: "4",
    title: "Product Designer",
    company: "DesignHub",
    location: "Remote",
    type: "Full-time",
    salary: "$110k - $150k",
    experience: "3+ years",
    postedDate: "5 days ago",
    description:
      "We are looking for a creative Product Designer to help us craft beautiful and intuitive user experiences. You will work closely with product managers and engineers to bring ideas to life.",
    responsibilities: [
      "Create user-centered designs for web and mobile applications",
      "Conduct user research and usability testing",
      "Develop wireframes, prototypes, and high-fidelity mockups",
      "Collaborate with cross-functional teams throughout the design process",
      "Maintain and evolve our design system",
    ],
    requirements: [
      "3+ years of product design experience",
      "Strong portfolio demonstrating UX/UI design skills",
      "Proficiency in Figma and other design tools",
      "Understanding of design systems and component libraries",
      "Excellent communication and presentation skills",
    ],
    benefits: [
      "Fully remote position",
      "Competitive salary",
      "Health insurance",
      "Equipment and software budget",
      "Flexible working hours",
    ],
  },
  {
    id: "5",
    title: "Backend Engineer",
    company: "API Masters",
    location: "Seattle, WA",
    type: "Full-time",
    salary: "$135k - $175k",
    experience: "4+ years",
    postedDate: "1 day ago",
    description:
      "Join our backend team and help us build scalable, high-performance APIs that power our platform. You will work with modern technologies and solve challenging technical problems.",
    responsibilities: [
      "Design and implement scalable backend services and APIs",
      "Optimize database queries and improve system performance",
      "Write comprehensive tests and documentation",
      "Collaborate with frontend engineers on API design",
      "Monitor and troubleshoot production systems",
    ],
    requirements: [
      "4+ years of backend development experience",
      "Strong proficiency in Node.js, Python, or Go",
      "Experience with PostgreSQL, MongoDB, or similar databases",
      "Understanding of microservices architecture",
      "Knowledge of caching strategies and message queues",
    ],
    benefits: [
      "Competitive compensation",
      "Equity package",
      "Comprehensive health benefits",
      "Flexible PTO policy",
      "Professional growth opportunities",
    ],
  },
  {
    id: "6",
    title: "Mobile Developer",
    company: "AppCraft Studios",
    location: "Los Angeles, CA",
    type: "Full-time",
    salary: "$125k - $165k",
    experience: "3+ years",
    postedDate: "4 days ago",
    description:
      "We are seeking a skilled Mobile Developer to build amazing mobile experiences for iOS and Android. You will work on innovative features and help shape the future of our mobile platform.",
    responsibilities: [
      "Develop and maintain mobile applications for iOS and Android",
      "Implement new features and improve existing functionality",
      "Ensure app performance, quality, and responsiveness",
      "Collaborate with designers and backend engineers",
      "Stay up-to-date with mobile development trends",
    ],
    requirements: [
      "3+ years of mobile development experience",
      "Proficiency in React Native or Flutter",
      "Experience with native iOS (Swift) or Android (Kotlin) development",
      "Understanding of mobile app architecture patterns",
      "Published apps in App Store or Google Play",
    ],
    benefits: [
      "Competitive salary and equity",
      "Health and wellness benefits",
      "Hybrid work model",
      "Latest mobile devices for testing",
      "Conference and training budget",
    ],
  },
];
