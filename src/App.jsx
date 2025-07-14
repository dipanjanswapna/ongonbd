import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import './App.css'

// Import components
import Navbar from './components/Navbar'
import Footer from './components/Footer'

// Import pages
import HomePage from './components/pages/HomePage'
import LoginPage from './components/pages/LoginPage'
import RegisterPage from './components/pages/RegisterPage'
import DashboardPage from './components/pages/DashboardPage'

// Context for authentication and global state
import { AuthProvider } from './contexts/AuthContext'
import { ThemeProvider } from './contexts/ThemeContext'
import { NotificationProvider } from './contexts/NotificationContext'

// Simple placeholder components
const EducationPage = () => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Education</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">শিক্ষা</p>
        <p className="text-gray-700 dark:text-gray-300">
          Comprehensive education platform with courses, scholarships, and learning resources.
        </p>
      </div>
    </div>
  </div>
)

const HealthcarePage = () => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Healthcare</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">স্বাস্থ্যসেবা</p>
        <p className="text-gray-700 dark:text-gray-300">
          Telemedicine, health records, and community health services.
        </p>
      </div>
    </div>
  </div>
)

const AgriculturePage = () => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Agriculture</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">কৃষি</p>
        <p className="text-gray-700 dark:text-gray-300">
          Smart farming solutions, crop management, and agricultural resources.
        </p>
      </div>
    </div>
  </div>
)

const BusinessPage = () => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Business</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">ব্যবসা</p>
        <p className="text-gray-700 dark:text-gray-300">
          Microfinance, business development, and entrepreneurship support.
        </p>
      </div>
    </div>
  </div>
)

const CommunityPage = () => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Community</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">সম্প্রদায়</p>
        <p className="text-gray-700 dark:text-gray-300">
          Social networking, community projects, and collaborative initiatives.
        </p>
      </div>
    </div>
  </div>
)

const ProjectsPage = () => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Projects</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">প্রকল্প</p>
        <p className="text-gray-700 dark:text-gray-300">
          Development projects, donations, and community initiatives.
        </p>
      </div>
    </div>
  </div>
)

const ProfilePage = () => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Profile</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">প্রোফাইল</p>
        <p className="text-gray-700 dark:text-gray-300">
          User profile management and personal settings.
        </p>
      </div>
    </div>
  </div>
)

const SettingsPage = () => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">Settings</h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">সেটিংস</p>
        <p className="text-gray-700 dark:text-gray-300">
          Application settings and preferences.
        </p>
      </div>
    </div>
  </div>
)

// Loading component
const LoadingSpinner = () => (
  <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
    <div className="text-center">
      <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-green-600 mx-auto mb-4"></div>
      <h2 className="text-2xl font-bold text-green-600 mb-2">ONGON BANGLADESH</h2>
      <p className="text-gray-600 dark:text-gray-400">সামাজিক কল্যাণ ও উন্নয়ন প্ল্যাটফর্ম</p>
      <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">Loading your personalized experience...</p>
    </div>
  </div>
)

function App() {
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate loading time
    const timer = setTimeout(() => {
      setLoading(false)
    }, 2000)

    return () => clearTimeout(timer)
  }, [])

  if (loading) {
    return <LoadingSpinner />
  }

  return (
    <AuthProvider>
      <ThemeProvider>
        <NotificationProvider>
          <Router>
            <div className="App min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white transition-colors duration-300">
              <Navbar />
              
              <AnimatePresence mode="wait">
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />
                  <Route path="/dashboard" element={<DashboardPage />} />
                  <Route path="/education" element={<EducationPage />} />
                  <Route path="/healthcare" element={<HealthcarePage />} />
                  <Route path="/agriculture" element={<AgriculturePage />} />
                  <Route path="/business" element={<BusinessPage />} />
                  <Route path="/community" element={<CommunityPage />} />
                  <Route path="/projects" element={<ProjectsPage />} />
                  <Route path="/profile" element={<ProfilePage />} />
                  <Route path="/settings" element={<SettingsPage />} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </AnimatePresence>
              
              <Footer />
            </div>
          </Router>
        </NotificationProvider>
      </ThemeProvider>
    </AuthProvider>
  )
}

export default App

