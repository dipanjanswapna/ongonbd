// API configuration and service functions
const API_BASE_URL = 'http://localhost:5000/api'

// API client with error handling
class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    // Add authorization header if token exists
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }

    try {
      const response = await fetch(url, config)
      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.message || `HTTP error! status: ${response.status}`)
      }

      return data
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // GET request
  async get(endpoint, options = {}) {
    return this.request(endpoint, { method: 'GET', ...options })
  }

  // POST request
  async post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
      ...options,
    })
  }

  // PUT request
  async put(endpoint, data, options = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
      ...options,
    })
  }

  // DELETE request
  async delete(endpoint, options = {}) {
    return this.request(endpoint, { method: 'DELETE', ...options })
  }
}

// Create API client instance
const apiClient = new ApiClient()

// Authentication API functions
export const authAPI = {
  // User registration
  register: async (userData) => {
    return apiClient.post('/auth/register', userData)
  },

  // User login
  login: async (credentials) => {
    return apiClient.post('/auth/login', credentials)
  },

  // User logout
  logout: async () => {
    return apiClient.post('/auth/logout')
  },

  // Refresh token
  refreshToken: async () => {
    return apiClient.post('/auth/refresh')
  },

  // Get current user profile
  getCurrentUser: async () => {
    return apiClient.get('/auth/me')
  },

  // Update user profile
  updateProfile: async (profileData) => {
    return apiClient.put('/auth/profile', profileData)
  },

  // Change password
  changePassword: async (passwordData) => {
    return apiClient.put('/auth/change-password', passwordData)
  },

  // Forgot password
  forgotPassword: async (email) => {
    return apiClient.post('/auth/forgot-password', { email })
  },

  // Reset password
  resetPassword: async (resetData) => {
    return apiClient.post('/auth/reset-password', resetData)
  },

  // Verify email
  verifyEmail: async (token) => {
    return apiClient.post('/auth/verify-email', { token })
  },

  // Resend verification email
  resendVerification: async (email) => {
    return apiClient.post('/auth/resend-verification', { email })
  }
}

// User API functions
export const userAPI = {
  // Get user profile
  getProfile: async (userId) => {
    return apiClient.get(`/users/${userId}`)
  },

  // Update user profile
  updateProfile: async (userId, profileData) => {
    return apiClient.put(`/users/${userId}`, profileData)
  },

  // Get user activities
  getActivities: async (userId, params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/users/${userId}/activities?${queryString}`)
  },

  // Get user statistics
  getStats: async (userId) => {
    return apiClient.get(`/users/${userId}/stats`)
  },

  // Upload profile picture
  uploadProfilePicture: async (userId, file) => {
    const formData = new FormData()
    formData.append('profile_picture', file)
    
    return apiClient.request(`/users/${userId}/profile-picture`, {
      method: 'POST',
      body: formData,
      headers: {} // Remove Content-Type to let browser set it for FormData
    })
  }
}

// Education API functions
export const educationAPI = {
  // Get courses
  getCourses: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/education/courses?${queryString}`)
  },

  // Get course details
  getCourse: async (courseId) => {
    return apiClient.get(`/education/courses/${courseId}`)
  },

  // Enroll in course
  enrollCourse: async (courseId) => {
    return apiClient.post(`/education/courses/${courseId}/enroll`)
  },

  // Get enrollments
  getEnrollments: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/education/enrollments?${queryString}`)
  },

  // Get scholarships
  getScholarships: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/education/scholarships?${queryString}`)
  },

  // Apply for scholarship
  applyScholarship: async (scholarshipId, applicationData) => {
    return apiClient.post(`/education/scholarships/${scholarshipId}/apply`, applicationData)
  }
}

// Healthcare API functions
export const healthcareAPI = {
  // Get health records
  getHealthRecords: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/healthcare/records?${queryString}`)
  },

  // Create health record
  createHealthRecord: async (recordData) => {
    return apiClient.post('/healthcare/records', recordData)
  },

  // Get appointments
  getAppointments: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/healthcare/appointments?${queryString}`)
  },

  // Book appointment
  bookAppointment: async (appointmentData) => {
    return apiClient.post('/healthcare/appointments', appointmentData)
  },

  // Get health camps
  getHealthCamps: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/healthcare/camps?${queryString}`)
  }
}

// Agriculture API functions
export const agricultureAPI = {
  // Get crops
  getCrops: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/agriculture/crops?${queryString}`)
  },

  // Create crop record
  createCrop: async (cropData) => {
    return apiClient.post('/agriculture/crops', cropData)
  },

  // Get weather data
  getWeatherData: async (location) => {
    return apiClient.get(`/agriculture/weather?location=${encodeURIComponent(location)}`)
  },

  // Get market prices
  getMarketPrices: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/agriculture/market-prices?${queryString}`)
  }
}

// Business API functions
export const businessAPI = {
  // Get businesses
  getBusinesses: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/business/businesses?${queryString}`)
  },

  // Create business
  createBusiness: async (businessData) => {
    return apiClient.post('/business/businesses', businessData)
  },

  // Get jobs
  getJobs: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/business/jobs?${queryString}`)
  },

  // Apply for job
  applyJob: async (jobId, applicationData) => {
    return apiClient.post(`/business/jobs/${jobId}/apply`, applicationData)
  },

  // Get loans
  getLoans: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/business/loans?${queryString}`)
  },

  // Apply for loan
  applyLoan: async (loanData) => {
    return apiClient.post('/business/loans/apply', loanData)
  }
}

// Community API functions
export const communityAPI = {
  // Get forums
  getForums: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/community/forums?${queryString}`)
  },

  // Get forum posts
  getForumPosts: async (forumId, params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/community/forums/${forumId}/posts?${queryString}`)
  },

  // Create forum post
  createForumPost: async (forumId, postData) => {
    return apiClient.post(`/community/forums/${forumId}/posts`, postData)
  },

  // Get events
  getEvents: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/community/events?${queryString}`)
  },

  // Register for event
  registerEvent: async (eventId) => {
    return apiClient.post(`/community/events/${eventId}/register`)
  },

  // Get volunteer opportunities
  getVolunteerOpportunities: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/community/volunteer?${queryString}`)
  },

  // Apply for volunteer opportunity
  applyVolunteer: async (opportunityId, applicationData) => {
    return apiClient.post(`/community/volunteer/${opportunityId}/apply`, applicationData)
  }
}

// Projects API functions
export const projectsAPI = {
  // Get projects
  getProjects: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/projects?${queryString}`)
  },

  // Get project details
  getProject: async (projectId) => {
    return apiClient.get(`/projects/${projectId}`)
  },

  // Create project
  createProject: async (projectData) => {
    return apiClient.post('/projects', projectData)
  },

  // Update project
  updateProject: async (projectId, projectData) => {
    return apiClient.put(`/projects/${projectId}`, projectData)
  },

  // Donate to project
  donateToProject: async (projectId, donationData) => {
    return apiClient.post(`/projects/${projectId}/donate`, donationData)
  },

  // Get donations
  getDonations: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/donations?${queryString}`)
  },

  // Get project updates
  getProjectUpdates: async (projectId, params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/projects/${projectId}/updates?${queryString}`)
  },

  // Create project update
  createProjectUpdate: async (projectId, updateData) => {
    return apiClient.post(`/projects/${projectId}/updates`, updateData)
  }
}

// Utility functions
export const utilsAPI = {
  // Health check
  healthCheck: async () => {
    return apiClient.get('/health')
  },

  // Upload file
  uploadFile: async (file, type = 'general') => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('type', type)
    
    return apiClient.request('/upload', {
      method: 'POST',
      body: formData,
      headers: {} // Remove Content-Type to let browser set it for FormData
    })
  },

  // Get notifications
  getNotifications: async (params = {}) => {
    const queryString = new URLSearchParams(params).toString()
    return apiClient.get(`/notifications?${queryString}`)
  },

  // Mark notification as read
  markNotificationRead: async (notificationId) => {
    return apiClient.put(`/notifications/${notificationId}/read`)
  },

  // Get statistics
  getStatistics: async () => {
    return apiClient.get('/statistics')
  }
}

export default apiClient

