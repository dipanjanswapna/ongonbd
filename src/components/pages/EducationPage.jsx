import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  GraduationCap, 
  BookOpen, 
  Users, 
  Award, 
  Search, 
  Filter, 
  Star,
  Clock,
  Play,
  Download,
  Heart,
  Share2,
  ChevronRight,
  TrendingUp,
  Target,
  Calendar
} from 'lucide-react'
import { useAuth } from '../../contexts/AuthContext'
import { useNotification } from '../../contexts/NotificationContext'

const EducationPage = () => {
  const { isAuthenticated, user } = useAuth()
  const { showNotification } = useNotification()
  const [activeTab, setActiveTab] = useState('courses')
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

  // Mock data for courses
  const courses = [
    {
      id: 1,
      title: 'Digital Literacy for Rural Communities',
      titleBn: 'গ্রামীণ সম্প্রদায়ের জন্য ডিজিটাল সাক্ষরতা',
      description: 'Learn essential computer and internet skills to participate in the digital economy.',
      instructor: 'Dr. Rashida Khan',
      duration: '6 weeks',
      level: 'Beginner',
      rating: 4.8,
      students: 1250,
      price: 'Free',
      image: '/api/placeholder/300/200',
      category: 'technology',
      lessons: 24,
      certificate: true
    },
    {
      id: 2,
      title: 'Sustainable Agriculture Practices',
      titleBn: 'টেকসই কৃষি অনুশীলন',
      description: 'Modern farming techniques for better yield and environmental protection.',
      instructor: 'Prof. Abdul Karim',
      duration: '8 weeks',
      level: 'Intermediate',
      rating: 4.9,
      students: 890,
      price: 'Free',
      image: '/api/placeholder/300/200',
      category: 'agriculture',
      lessons: 32,
      certificate: true
    },
    {
      id: 3,
      title: 'Small Business Management',
      titleBn: 'ছোট ব্যবসা ব্যবস্থাপনা',
      description: 'Learn to start and manage your own small business effectively.',
      instructor: 'Fatima Ahmed',
      duration: '4 weeks',
      level: 'Beginner',
      rating: 4.7,
      students: 2100,
      price: 'Free',
      image: '/api/placeholder/300/200',
      category: 'business',
      lessons: 18,
      certificate: true
    },
    {
      id: 4,
      title: 'Healthcare Basics for Communities',
      titleBn: 'সম্প্রদায়ের জন্য স্বাস্থ্যসেবার মূল বিষয়',
      description: 'Essential health knowledge and first aid for community health workers.',
      instructor: 'Dr. Mohammad Hasan',
      duration: '5 weeks',
      level: 'Beginner',
      rating: 4.8,
      students: 1560,
      price: 'Free',
      image: '/api/placeholder/300/200',
      category: 'healthcare',
      lessons: 20,
      certificate: true
    }
  ]

  // Mock data for scholarships
  const scholarships = [
    {
      id: 1,
      title: 'Rural Education Excellence Scholarship',
      titleBn: 'গ্রামীণ শিক্ষা উৎকর্ষতা বৃত্তি',
      amount: '৳50,000',
      deadline: '2025-08-15',
      eligibility: 'Students from rural areas with excellent academic records',
      applicants: 245,
      available: 25
    },
    {
      id: 2,
      title: 'Women Empowerment Education Grant',
      titleBn: 'নারী ক্ষমতায়ন শিক্ষা অনুদান',
      amount: '৳75,000',
      deadline: '2025-09-30',
      eligibility: 'Female students pursuing higher education',
      applicants: 189,
      available: 15
    },
    {
      id: 3,
      title: 'Technology Skills Development Fund',
      titleBn: 'প্রযুক্তি দক্ষতা উন্নয়ন তহবিল',
      amount: '৳30,000',
      deadline: '2025-07-20',
      eligibility: 'Students interested in technology and programming',
      applicants: 156,
      available: 30
    }
  ]

  const categories = [
    { id: 'all', name: 'All Courses', nameBn: 'সব কোর্স' },
    { id: 'technology', name: 'Technology', nameBn: 'প্রযুক্তি' },
    { id: 'agriculture', name: 'Agriculture', nameBn: 'কৃষি' },
    { id: 'business', name: 'Business', nameBn: 'ব্যবসা' },
    { id: 'healthcare', name: 'Healthcare', nameBn: 'স্বাস্থ্যসেবা' }
  ]

  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         course.titleBn.includes(searchQuery)
    const matchesCategory = selectedCategory === 'all' || course.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const handleEnrollCourse = (courseId) => {
    if (!isAuthenticated()) {
      showNotification('Please login to enroll in courses', 'warning')
      return
    }
    showNotification('Course enrollment functionality coming soon!', 'info')
  }

  const handleApplyScholarship = (scholarshipId) => {
    if (!isAuthenticated()) {
      showNotification('Please login to apply for scholarships', 'warning')
      return
    }
    showNotification('Scholarship application functionality coming soon!', 'info')
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-16">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-green-600 to-blue-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center"
          >
            <div className="flex justify-center mb-6">
              <div className="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center">
                <GraduationCap className="w-10 h-10" />
              </div>
            </div>
            <h1 className="text-4xl md:text-6xl font-bold mb-4">
              Education
            </h1>
            <p className="text-xl mb-2">শিক্ষা</p>
            <p className="text-lg max-w-3xl mx-auto mb-8">
              Empowering communities through accessible, quality education. 
              Learn new skills, advance your career, and build a better future.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={() => setActiveTab('courses')}
                className="bg-white text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Browse Courses
              </button>
              <button 
                onClick={() => setActiveTab('scholarships')}
                className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-green-600 transition-colors"
              >
                View Scholarships
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-center"
            >
              <div className="text-3xl font-bold text-green-600 mb-2">5,800+</div>
              <div className="text-gray-600 dark:text-gray-400">Students Enrolled</div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-center"
            >
              <div className="text-3xl font-bold text-blue-600 mb-2">150+</div>
              <div className="text-gray-600 dark:text-gray-400">Courses Available</div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-center"
            >
              <div className="text-3xl font-bold text-purple-600 mb-2">95%</div>
              <div className="text-gray-600 dark:text-gray-400">Completion Rate</div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="text-center"
            >
              <div className="text-3xl font-bold text-orange-600 mb-2">70+</div>
              <div className="text-gray-600 dark:text-gray-400">Scholarships Given</div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Tab Navigation */}
          <div className="flex flex-wrap gap-4 mb-8 border-b border-gray-200 dark:border-gray-700">
            <button
              onClick={() => setActiveTab('courses')}
              className={`px-6 py-3 font-semibold border-b-2 transition-colors ${
                activeTab === 'courses'
                  ? 'border-green-500 text-green-600 dark:text-green-400'
                  : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
            >
              <BookOpen className="w-5 h-5 inline mr-2" />
              Courses
            </button>
            <button
              onClick={() => setActiveTab('scholarships')}
              className={`px-6 py-3 font-semibold border-b-2 transition-colors ${
                activeTab === 'scholarships'
                  ? 'border-green-500 text-green-600 dark:text-green-400'
                  : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
            >
              <Award className="w-5 h-5 inline mr-2" />
              Scholarships
            </button>
            <button
              onClick={() => setActiveTab('progress')}
              className={`px-6 py-3 font-semibold border-b-2 transition-colors ${
                activeTab === 'progress'
                  ? 'border-green-500 text-green-600 dark:text-green-400'
                  : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
              }`}
            >
              <TrendingUp className="w-5 h-5 inline mr-2" />
              My Progress
            </button>
          </div>

          {/* Courses Tab */}
          {activeTab === 'courses' && (
            <div>
              {/* Search and Filter */}
              <div className="flex flex-col md:flex-row gap-4 mb-8">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      placeholder="Search courses..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                    />
                  </div>
                </div>
                <div className="flex gap-2 flex-wrap">
                  {categories.map((category) => (
                    <button
                      key={category.id}
                      onClick={() => setSelectedCategory(category.id)}
                      className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                        selectedCategory === category.id
                          ? 'bg-green-600 text-white'
                          : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                      }`}
                    >
                      {category.name}
                    </button>
                  ))}
                </div>
              </div>

              {/* Course Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredCourses.map((course) => (
                  <motion.div
                    key={course.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
                  >
                    <div className="h-48 bg-gradient-to-r from-green-400 to-blue-500 flex items-center justify-center">
                      <BookOpen className="w-16 h-16 text-white" />
                    </div>
                    <div className="p-6">
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs font-semibold text-green-600 bg-green-100 dark:bg-green-900 px-2 py-1 rounded">
                          {course.level}
                        </span>
                        <div className="flex items-center text-yellow-500">
                          <Star className="w-4 h-4 fill-current" />
                          <span className="text-sm ml-1">{course.rating}</span>
                        </div>
                      </div>
                      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-1">
                        {course.title}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                        {course.titleBn}
                      </p>
                      <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 line-clamp-2">
                        {course.description}
                      </p>
                      <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400 mb-4">
                        <div className="flex items-center">
                          <Clock className="w-4 h-4 mr-1" />
                          {course.duration}
                        </div>
                        <div className="flex items-center">
                          <Users className="w-4 h-4 mr-1" />
                          {course.students}
                        </div>
                      </div>
                      <div className="flex items-center justify-between">
                        <div>
                          <span className="text-lg font-bold text-green-600">{course.price}</span>
                          {course.certificate && (
                            <div className="flex items-center text-xs text-gray-500 dark:text-gray-400 mt-1">
                              <Award className="w-3 h-3 mr-1" />
                              Certificate
                            </div>
                          )}
                        </div>
                        <button
                          onClick={() => handleEnrollCourse(course.id)}
                          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors flex items-center"
                        >
                          Enroll Now
                          <ChevronRight className="w-4 h-4 ml-1" />
                        </button>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}

          {/* Scholarships Tab */}
          {activeTab === 'scholarships' && (
            <div className="space-y-6">
              {scholarships.map((scholarship) => (
                <motion.div
                  key={scholarship.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6"
                >
                  <div className="flex flex-col md:flex-row md:items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <Award className="w-6 h-6 text-yellow-500 mr-2" />
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white">
                          {scholarship.title}
                        </h3>
                      </div>
                      <p className="text-gray-600 dark:text-gray-400 mb-2">
                        {scholarship.titleBn}
                      </p>
                      <p className="text-gray-700 dark:text-gray-300 mb-4">
                        {scholarship.eligibility}
                      </p>
                      <div className="flex flex-wrap gap-4 text-sm">
                        <div className="flex items-center text-green-600">
                          <Target className="w-4 h-4 mr-1" />
                          Amount: {scholarship.amount}
                        </div>
                        <div className="flex items-center text-blue-600">
                          <Calendar className="w-4 h-4 mr-1" />
                          Deadline: {scholarship.deadline}
                        </div>
                        <div className="flex items-center text-purple-600">
                          <Users className="w-4 h-4 mr-1" />
                          {scholarship.applicants} applicants
                        </div>
                      </div>
                    </div>
                    <div className="mt-4 md:mt-0 md:ml-6">
                      <div className="text-center mb-4">
                        <div className="text-2xl font-bold text-green-600">
                          {scholarship.available}
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          Available
                        </div>
                      </div>
                      <button
                        onClick={() => handleApplyScholarship(scholarship.id)}
                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors w-full md:w-auto"
                      >
                        Apply Now
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}

          {/* Progress Tab */}
          {activeTab === 'progress' && (
            <div className="text-center py-12">
              {isAuthenticated() ? (
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
                  <TrendingUp className="w-16 h-16 text-green-600 mx-auto mb-4" />
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    Your Learning Progress
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-6">
                    Track your course progress, certificates, and achievements here.
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    🚧 Progress tracking functionality coming soon!
                  </p>
                </div>
              ) : (
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">
                  <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    Login Required
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-6">
                    Please login to view your learning progress and achievements.
                  </p>
                  <a
                    href="/login"
                    className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors inline-flex items-center"
                  >
                    Login Now
                    <ChevronRight className="w-4 h-4 ml-2" />
                  </a>
                </div>
              )}
            </div>
          )}
        </div>
      </section>
    </div>
  )
}

export default EducationPage

