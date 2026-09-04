import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserProfile, Role } from '../types';

interface AuthContextType {
  user: UserProfile | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, role: Role, name: string, token: string, establishmentId?: string) => void;
  logout: () => void;
  switchPersona: (role: Role) => void;
}

const DEMO_PROFILES: Record<Role, UserProfile> = {
  inspector: {
    id: "USR-INSP-01",
    email: "inspector@shram.gov.in",
    name: "S. K. Sharma",
    role: "inspector",
    designation: "Assistant Labour Commissioner (Central)",
    jurisdiction: "Delhi & NCR Region",
  },
  employer: {
    id: "USR-EMP-01",
    email: "employer@abcindustries.com",
    name: "Rajiv Mehra",
    role: "employer",
    designation: "Compliance Officer & Factory Manager",
    establishment_id: "EST-001",
  },
  admin: {
    id: "USR-ADM-01",
    email: "admin@shram.gov.in",
    name: "Dr. V. Ramanathan",
    role: "admin",
    designation: "Chief Labour Intelligence Administrator",
    jurisdiction: "National Enforcement Sphere",
  },
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(() => {
    try {
      const saved = localStorage.getItem('shram_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });

  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('shram_token') || null;
  });

  useEffect(() => {
    if (user) {
      localStorage.setItem('shram_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('shram_user');
    }
  }, [user]);

  const login = (email: string, role: Role, name: string, tokenStr: string, establishmentId?: string) => {
    const defaultProfile = DEMO_PROFILES[role] || {
      id: `USR-${role.toUpperCase()}`,
      email,
      name,
      role,
      designation: role.toUpperCase(),
      establishment_id: establishmentId,
    };
    const profile: UserProfile = {
      ...defaultProfile,
      email,
      name,
      role,
      establishment_id: establishmentId !== undefined ? establishmentId : defaultProfile.establishment_id,
    };
    setUser(profile);
    setToken(tokenStr);
    localStorage.setItem('shram_token', tokenStr);
    localStorage.setItem('shram_user', JSON.stringify(profile));
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('shram_user');
    localStorage.removeItem('shram_token');
    sessionStorage.clear();
  };

  const switchPersona = (role: Role) => {
    const profile = DEMO_PROFILES[role];
    setUser(profile);
    const mockToken = `jwt-token-${role}`;
    setToken(mockToken);
    localStorage.setItem('shram_token', mockToken);
    localStorage.setItem('shram_user', JSON.stringify(profile));
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        login,
        logout,
        switchPersona,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
