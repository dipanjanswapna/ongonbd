import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  ArrowRight, 
  Play, 
  Users, 
  Target, 
  Award, 
  TrendingUp,
  GraduationCap,
  Heart,
  Sprout,
  Briefcase,
  HandHeart,
  Globe,
  Star,
  ChevronLeft,
  ChevronRight,
  Quote
} from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { useAuth } from '../../contexts/AuthContext'

const HomePage = () => {
  const { isAuthenticated } = useAuth()
  const [currentTestimonial, setCurrentTestimonial] = useState(0)

  // Auto-rotate testimonials
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length)
    }, 5000)
    return () => clearInterval(timer)
  }, [])

  const features = [
    {
      icon: GraduationCap,
      title: 'Education',
      description: 'Comprehensive learning platform with courses, scholarships, and skill development programs.',
      color: 'from-blue-500 to-blue-600',
      stats: '10,000+ Students'
    },
    {
      icon: Heart,
      title: 'Healthcare',
      description: 'Telemedicine, health camps, blood donation drives, and medical assistance programs.',
      color: 'from-red-500 to-red-600',
      stats: '25,000+ Patients'
    },
    {
      icon: Sprout,
      title: 'Agriculture',
      description: 'Modern farming techniques, crop management, and agricultural marketplace.',
      color: 'from-green-500 to-green-600',
      stats: '5,000+ Farmers'
    },
    {
      icon: Briefcase,
      title: 'Business',
      description: 'Microfinance, job portal, training programs, and entrepreneurship support.',
      color: 'from-purple-500 to-purple-600',
      stats: '15,000+ Entrepreneurs'
    },
    {
      icon: Users,
      title: 'Community',
      description: 'Forums, events, volunteer opportunities, and social networking.',
      color: 'from-orange-500 to-orange-600',
      stats: '50,000+ Members'
    },
    {
      icon: Target,
      title: 'Projects',
      description: 'Crowdfunding, donation management, and social impact projects.',
      color: 'from-indigo-500 to-indigo-600',
      stats: '1,200+ Projects'
    }
  ]

  const stats = [
    { icon: Users, label: 'Active Users', value: '50,000+', color: 'text-blue-600' },
    { icon: Target, label: 'Projects Completed', value: '1,200+', color: 'text-green-600' },
    { icon: Award, label: 'Lives Impacted', value: '100,000+', color: 'text-purple-600' },
    { icon: Globe, label: 'Communities Served', value: '500+', color: 'text-orange-600' }
  ]

  const testimonials = [
    {
      name: 'রহিমা খাতুন',
      role: 'Farmer from Rangpur',
      content: 'ONGON BANGLADESH এর মাধ্যমে আমি আধুনিক কৃষি পদ্ধতি শিখেছি এবং আমার ফসলের উৎপাদন দ্বিগুণ হয়েছে।',
      rating: 5,
      image: '/api/placeholder/60/60'
    },
    {
      name: 'ডাঃ করিম উদ্দিন',
      role: 'Healthcare Provider',
      content: 'This platform has revolutionized healthcare delivery in rural areas. We can now reach patients who never had access to medical care.',
      rating: 5,
      image: '/api/placeholder/60/60'
    },
    {
      name: 'ফাতেমা বেগম',
      role: 'Student from Sylhet',
      content: 'The education modules helped me develop new skills and I got a scholarship for higher studies. Thank you ONGON BANGLADESH!',
      rating: 5,
      image: '/api/placeholder/60/60'
    }
  ]

  const recentProjects = [
    {
      title: 'Clean Water Initiative',
      description: 'Providing clean drinking water to 50 villages in rural Bangladesh',
      raised: 850000,
      target: 1000000,
      image: '/api/placeholder/300/200',
      category: 'Healthcare'
    },
    {
      title: 'Digital Literacy Program',
      description: 'Teaching computer skills to 1000 rural students',
      raised: 450000,
      target: 500000,
      image: '/api/placeholder/300/200',
      category: 'Education'
    },
    {
      title: 'Sustainable Farming',
      description: 'Training farmers in organic farming techniques',
      raised: 320000,
      target: 400000,
      image: '/api/placeholder/300/200',
      category: 'Agriculture'
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 overflow-hidden">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0 bg-gradient-to-br from-green-100 to-blue-100 dark:from-gray-800 dark:to-gray-700"></div>
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <Badge className="mb-6 px-4 py-2 text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
              🇧🇩 Empowering Bangladesh Together
            </Badge>
            
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-6">
              <span className="bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
                ONGON BANGLADESH
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-green-700 dark:text-green-300 mb-4 font-medium">
              সামাজিক কল্যাণ ও উন্নয়ন প্ল্যাটফর্ম
            </p>
            
            <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              A comprehensive platform connecting communities through education, healthcare, agriculture, 
              and social development. Together, we build a stronger, more prosperous Bangladesh.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              {isAuthenticated ? (
                <Button asChild size="lg" className="px-8 py-4 text-lg">
                  <Link to="/dashboard">
                    Go to Dashboard
                    <ArrowRight className="ml-2 w-5 h-5" />
                  </Link>
                </Button>
              ) : (
                <>
                  <Button asChild size="lg" className="px-8 py-4 text-lg">
                    <Link to="/register">
                      Get Started
                      <ArrowRight className="ml-2 w-5 h-5" />
                    </Link>
                  </Button>
                  <Button variant="outline" size="lg" className="px-8 py-4 text-lg">
                    <Play className="mr-2 w-5 h-5" />
                    Watch Demo
                  </Button>
                </>
              )}
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 + index * 0.1 }}
                  className="text-center"
                >
                  <div className={`inline-flex items-center justify-center w-12 h-12 rounded-full bg-white dark:bg-gray-800 shadow-lg mb-3`}>
                    <stat.icon className={`w-6 h-6 ${stat.color}`} />
                  </div>
                  <div className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-1">
                    {stat.value}
                  </div>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    {stat.label}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ repeat: Infinity, duration: 2 }}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        >
          <div className="w-6 h-10 border-2 border-gray-400 rounded-full flex justify-center">
            <div className="w-1 h-3 bg-gray-400 rounded-full mt-2"></div>
          </div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Our Impact Areas
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Comprehensive solutions addressing the most critical needs of Bangladeshi communities
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -5 }}
                className="group"
              >
                <Card className="h-full border-0 shadow-lg hover:shadow-xl transition-all duration-300">
                  <CardContent className="p-6">
                    <div className={`inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.color} mb-6 group-hover:scale-110 transition-transform duration-300`}>
                      <feature.icon className="w-8 h-8 text-white" />
                    </div>
                    
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                      {feature.title}
                    </h3>
                    
                    <p className="text-gray-600 dark:text-gray-300 mb-4">
                      {feature.description}
                    </p>
                    
                    <div className="flex items-center justify-between">
                      <Badge variant="secondary" className="text-xs">
                        {feature.stats}
                      </Badge>
                      <Button variant="ghost" size="sm" asChild>
                        <Link to={`/${feature.title.toLowerCase()}`}>
                          Learn More
                          <ArrowRight className="ml-1 w-4 h-4" />
                        </Link>
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Recent Projects Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Featured Projects
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Supporting impactful initiatives that create lasting change in communities across Bangladesh
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {recentProjects.map((project, index) => (
              <motion.div
                key={project.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="group"
              >
                <Card className="overflow-hidden border-0 shadow-lg hover:shadow-xl transition-all duration-300">
                  <div className="relative overflow-hidden">
                    <img
                      src={project.image}
                      alt={project.title}
                      className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <Badge className="absolute top-4 left-4 bg-white/90 text-gray-800">
                      {project.category}
                    </Badge>
                  </div>
                  
                  <CardContent className="p-6">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                      {project.title}
                    </h3>
                    
                    <p className="text-gray-600 dark:text-gray-300 mb-4">
                      {project.description}
                    </p>
                    
                    {/* Progress Bar */}
                    <div className="mb-4">
                      <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
                        <span>৳{project.raised.toLocaleString()} raised</span>
                        <span>৳{project.target.toLocaleString()} goal</span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${(project.raised / project.target) * 100}%` }}
                        ></div>
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                        {Math.round((project.raised / project.target) * 100)}% funded
                      </div>
                    </div>
                    
                    <Button className="w-full" asChild>
                      <Link to="/projects">
                        Support Project
                        <HandHeart className="ml-2 w-4 h-4" />
                      </Link>
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          <div className="text-center mt-12">
            <Button variant="outline" size="lg" asChild>
              <Link to="/projects">
                View All Projects
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              What Our Community Says
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Real stories from people whose lives have been transformed through our platform
            </p>
          </motion.div>

          <div className="relative max-w-4xl mx-auto">
            <Card className="border-0 shadow-lg">
              <CardContent className="p-8 md:p-12">
                <div className="text-center">
                  <Quote className="w-12 h-12 text-green-500 mx-auto mb-6" />
                  
                  <motion.div
                    key={currentTestimonial}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -20 }}
                    transition={{ duration: 0.5 }}
                  >
                    <p className="text-lg md:text-xl text-gray-700 dark:text-gray-300 mb-6 italic">
                      "{testimonials[currentTestimonial].content}"
                    </p>
                    
                    <div className="flex items-center justify-center space-x-4">
                      <img
                        src={testimonials[currentTestimonial].image}
                        alt={testimonials[currentTestimonial].name}
                        className="w-12 h-12 rounded-full"
                      />
                      <div className="text-left">
                        <h4 className="font-semibold text-gray-900 dark:text-white">
                          {testimonials[currentTestimonial].name}
                        </h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {testimonials[currentTestimonial].role}
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex justify-center mt-4">
                      {[...Array(testimonials[currentTestimonial].rating)].map((_, i) => (
                        <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                      ))}
                    </div>
                  </motion.div>
                </div>
              </CardContent>
            </Card>

            {/* Navigation Buttons */}
            <button
              onClick={() => setCurrentTestimonial((prev) => prev === 0 ? testimonials.length - 1 : prev - 1)}
              className="absolute left-4 top-1/2 transform -translate-y-1/2 p-2 rounded-full bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300"
            >
              <ChevronLeft className="w-6 h-6 text-gray-600 dark:text-gray-300" />
            </button>
            
            <button
              onClick={() => setCurrentTestimonial((prev) => (prev + 1) % testimonials.length)}
              className="absolute right-4 top-1/2 transform -translate-y-1/2 p-2 rounded-full bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300"
            >
              <ChevronRight className="w-6 h-6 text-gray-600 dark:text-gray-300" />
            </button>

            {/* Dots Indicator */}
            <div className="flex justify-center mt-8 space-x-2">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentTestimonial(index)}
                  className={`w-3 h-3 rounded-full transition-all duration-300 ${
                    index === currentTestimonial 
                      ? 'bg-green-500' 
                      : 'bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-500'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-green-600 to-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Make a Difference?
            </h2>
            <p className="text-xl text-green-100 mb-8 max-w-3xl mx-auto">
              Join thousands of Bangladeshis who are already creating positive change in their communities.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              {!isAuthenticated && (
                <Button size="lg" variant="secondary" className="px-8 py-4 text-lg" asChild>
                  <Link to="/register">
                    Join Our Community
                    <Users className="ml-2 w-5 h-5" />
                  </Link>
                </Button>
              )}
              
              <Button size="lg" variant="outline" className="px-8 py-4 text-lg border-white text-white hover:bg-white hover:text-green-600" asChild>
                <Link to="/projects">
                  Explore Projects
                  <Target className="ml-2 w-5 h-5" />
                </Link>
              </Button>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default HomePage

