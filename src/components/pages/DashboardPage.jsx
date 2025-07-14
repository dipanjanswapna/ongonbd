import React from 'react'
import { motion } from 'framer-motion'
import { 
  BarChart3, 
  Users, 
  Target, 
  TrendingUp,
  GraduationCap,
  Heart,
  Sprout,
  Briefcase,
  Calendar,
  Bell
} from 'lucide-react'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useAuth } from '../../contexts/AuthContext'

const DashboardPage = () => {
  const { user } = useAuth()

  const stats = [
    { title: 'Active Projects', value: '12', icon: Target, color: 'text-blue-600', bg: 'bg-blue-100' },
    { title: 'Community Members', value: '1,247', icon: Users, color: 'text-green-600', bg: 'bg-green-100' },
    { title: 'Total Donations', value: '৳45,000', icon: TrendingUp, color: 'text-purple-600', bg: 'bg-purple-100' },
    { title: 'Events Attended', value: '8', icon: Calendar, color: 'text-orange-600', bg: 'bg-orange-100' }
  ]

  const recentActivities = [
    { title: 'Donated to Clean Water Initiative', time: '2 hours ago', type: 'donation' },
    { title: 'Joined Agriculture Training Program', time: '1 day ago', type: 'education' },
    { title: 'Volunteered for Health Camp', time: '3 days ago', type: 'volunteer' },
    { title: 'Completed Digital Literacy Course', time: '1 week ago', type: 'achievement' }
  ]

  const quickActions = [
    { title: 'Education', icon: GraduationCap, href: '/education', color: 'from-blue-500 to-blue-600' },
    { title: 'Healthcare', icon: Heart, href: '/healthcare', color: 'from-red-500 to-red-600' },
    { title: 'Agriculture', icon: Sprout, href: '/agriculture', color: 'from-green-500 to-green-600' },
    { title: 'Business', icon: Briefcase, href: '/business', color: 'from-purple-500 to-purple-600' }
  ]

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome back, {user?.first_name || 'User'}! 👋
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Here's what's happening in your community today
          </p>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                        {stat.title}
                      </p>
                      <p className="text-2xl font-bold text-gray-900 dark:text-white">
                        {stat.value}
                      </p>
                    </div>
                    <div className={`p-3 rounded-full ${stat.bg}`}>
                      <stat.icon className={`w-6 h-6 ${stat.color}`} />
                    </div>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="lg:col-span-2"
          >
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {quickActions.map((action) => (
                    <Button
                      key={action.title}
                      variant="outline"
                      className="h-24 flex flex-col items-center justify-center space-y-2 hover:shadow-md transition-all duration-300"
                      asChild
                    >
                      <a href={action.href}>
                        <div className={`p-2 rounded-lg bg-gradient-to-r ${action.color}`}>
                          <action.icon className="w-6 h-6 text-white" />
                        </div>
                        <span className="text-sm font-medium">{action.title}</span>
                      </a>
                    </Button>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Recent Activities */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card>
              <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle>Recent Activities</CardTitle>
                <Bell className="w-5 h-5 text-gray-400" />
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {recentActivities.map((activity, index) => (
                    <div key={index} className="flex items-start space-x-3">
                      <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 dark:text-white">
                          {activity.title}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          {activity.time}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
                <Button variant="outline" className="w-full mt-4">
                  View All Activities
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Featured Projects */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
          className="mt-8"
        >
          <Card>
            <CardHeader>
              <CardTitle>Featured Projects</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {[1, 2, 3].map((project) => (
                  <div key={project} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="w-full h-32 bg-gradient-to-r from-green-400 to-blue-500 rounded-lg mb-4"></div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                      Sample Project {project}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                      This is a sample project description that shows how projects are displayed.
                    </p>
                    <div className="flex items-center justify-between">
                      <Badge variant="secondary">Active</Badge>
                      <Button size="sm" variant="outline">
                        View Details
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

export default DashboardPage

