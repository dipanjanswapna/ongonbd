import React from 'react'
import { motion } from 'framer-motion'

// Placeholder component template
const PlaceholderPage = ({ title, description, icon: Icon }) => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center"
      >
        {Icon && (
          <div className="flex justify-center mb-8">
            <div className="p-6 bg-gradient-to-r from-green-500 to-blue-600 rounded-full">
              <Icon className="w-16 h-16 text-white" />
            </div>
          </div>
        )}
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          {title}
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
          {description}
        </p>
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 max-w-2xl mx-auto">
          <p className="text-gray-700 dark:text-gray-300">
            This page is currently under development. We're working hard to bring you comprehensive features for {title.toLowerCase()}.
          </p>
          <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <p className="text-sm text-blue-800 dark:text-blue-200">
              🚧 Coming Soon: Advanced features, interactive tools, and community integration
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  </div>
)

// Individual page components
import { GraduationCap, Heart, Sprout, Briefcase, Users, Target, User, Info, Phone } from 'lucide-react'

export const EducationPage = () => (
  <PlaceholderPage 
    title="Education" 
    description="Comprehensive learning platform with courses, scholarships, and skill development programs"
    icon={GraduationCap}
  />
)

export const HealthcarePage = () => (
  <PlaceholderPage 
    title="Healthcare" 
    description="Telemedicine, health camps, blood donation drives, and medical assistance programs"
    icon={Heart}
  />
)

export const AgriculturePage = () => (
  <PlaceholderPage 
    title="Agriculture" 
    description="Modern farming techniques, crop management, and agricultural marketplace"
    icon={Sprout}
  />
)

export const BusinessPage = () => (
  <PlaceholderPage 
    title="Business" 
    description="Microfinance, job portal, training programs, and entrepreneurship support"
    icon={Briefcase}
  />
)

export const CommunityPage = () => (
  <PlaceholderPage 
    title="Community" 
    description="Forums, events, volunteer opportunities, and social networking"
    icon={Users}
  />
)

export const ProjectsPage = () => (
  <PlaceholderPage 
    title="Projects" 
    description="Crowdfunding, donation management, and social impact projects"
    icon={Target}
  />
)

export const ProfilePage = () => (
  <PlaceholderPage 
    title="Profile" 
    description="Manage your account settings, preferences, and personal information"
    icon={User}
  />
)

export const AboutPage = () => (
  <PlaceholderPage 
    title="About Us" 
    description="Learn more about ONGON BANGLADESH and our mission to empower communities"
    icon={Info}
  />
)

export const ContactPage = () => (
  <PlaceholderPage 
    title="Contact Us" 
    description="Get in touch with our team for support, partnerships, or general inquiries"
    icon={Phone}
  />
)

export const NotFoundPage = () => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20 flex items-center justify-center">
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="text-center"
    >
      <div className="text-6xl font-bold text-gray-300 dark:text-gray-600 mb-4">404</div>
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
        Page Not Found
      </h1>
      <p className="text-gray-600 dark:text-gray-400 mb-8">
        The page you're looking for doesn't exist.
      </p>
      <a
        href="/"
        className="inline-flex items-center px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
      >
        Go Home
      </a>
    </motion.div>
  </div>
)

