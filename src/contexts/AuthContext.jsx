import React, { createContext, useContext, useState, useEffect } from 'react'
import { authAPI } from '../services/api'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Check if user is logged in on app start
  useEffect(() => {
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('authToken')
      if (token) {
        const userData = await authAPI.getCurrentUser()
        setUser(userData.user)
      }
    } catch (error) {
      console.error('Auth check failed:', error)
      localStorage.removeItem('authToken')
      localStorage.removeItem('refreshToken')
    } finally {
      setLoading(false)
    }
  }

  const login = async (credentials) => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await authAPI.login(credentials)
      
      // Store tokens
      localStorage.setItem('authToken', response.access_token)
      if (response.refresh_token) {
        localStorage.setItem('refreshToken', response.refresh_token)
      }
      
      // Set user data
      setUser(response.user)
      
      return { success: true, user: response.user }
    } catch (error) {
      setError(error.message)
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const register = async (userData) => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await authAPI.register(userData)
      
      // Store tokens if provided (auto-login after registration)
      if (response.access_token) {
        localStorage.setItem('authToken', response.access_token)
        if (response.refresh_token) {
          localStorage.setItem('refreshToken', response.refresh_token)
        }
        setUser(response.user)
      }
      
      return { success: true, user: response.user, message: response.message }
    } catch (error) {
      setError(error.message)
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // Clear local storage and state regardless of API call success
      localStorage.removeItem('authToken')
      localStorage.removeItem('refreshToken')
      setUser(null)
      setError(null)
    }
  }

  const updateProfile = async (profileData) => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await authAPI.updateProfile(profileData)
      setUser(response.user)
      
      return { success: true, user: response.user }
    } catch (error) {
      setError(error.message)
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const changePassword = async (passwordData) => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await authAPI.changePassword(passwordData)
      
      return { success: true, message: response.message }
    } catch (error) {
      setError(error.message)
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const forgotPassword = async (email) => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await authAPI.forgotPassword(email)
      
      return { success: true, message: response.message }
    } catch (error) {
      setError(error.message)
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const resetPassword = async (resetData) => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await authAPI.resetPassword(resetData)
      
      return { success: true, message: response.message }
    } catch (error) {
      setError(error.message)
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const verifyEmail = async (token) => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await authAPI.verifyEmail(token)
      
      // Update user data if verification affects user status
      if (response.user) {
        setUser(response.user)
      }
      
      return { success: true, message: response.message }
    } catch (error) {
      setError(error.message)
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const resendVerification = async (email) => {
    try {
      setLoading(true)
      setError(null)
      
      const response = await authAPI.resendVerification(email)
      
      return { success: true, message: response.message }
    } catch (error) {
      setError(error.message)
      return { success: false, error: error.message }
    } finally {
      setLoading(false)
    }
  }

  const refreshToken = async () => {
    try {
      const response = await authAPI.refreshToken()
      
      localStorage.setItem('authToken', response.access_token)
      if (response.refresh_token) {
        localStorage.setItem('refreshToken', response.refresh_token)
      }
      
      return response.access_token
    } catch (error) {
      console.error('Token refresh failed:', error)
      logout()
      throw error
    }
  }

  const clearError = () => {
    setError(null)
  }

  // Helper functions
  const isAuthenticated = () => {
    return !!user && !!localStorage.getItem('authToken')
  }

  const hasRole = (role) => {
    return user?.roles?.some(userRole => userRole.name === role) || false
  }

  const hasPermission = (permission) => {
    if (!user?.roles) return false
    
    return user.roles.some(role => 
      role.permissions?.some(perm => perm.name === permission)
    )
  }

  const getUserDisplayName = () => {
    if (!user) return 'Guest'
    return `${user.first_name} ${user.last_name}`.trim() || user.email || 'User'
  }

  const value = {
    // State
    user,
    loading,
    error,
    
    // Actions
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    forgotPassword,
    resetPassword,
    verifyEmail,
    resendVerification,
    refreshToken,
    clearError,
    
    // Helper functions
    isAuthenticated,
    hasRole,
    hasPermission,
    getUserDisplayName,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

