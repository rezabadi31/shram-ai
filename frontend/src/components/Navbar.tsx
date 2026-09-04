import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Building2, 
  FileSearch, 
  UploadCloud, 
  Bot, 
  LogOut, 
  ChevronDown, 
  FileCheck,
  Activity
} from 'lucide-react';
import { ActiveRole, SystemHealth } from '../types';
import { useAuth } from '../context/AuthContext';

interface NavbarProps {
  activeRole: ActiveRole;
  onSelectRole: (role: ActiveRole) => void;
  health: SystemHealth | null;
  onOpenAssistant: () => void;
  onOpenLogin: (role: 'employer' | 'inspector') => void;
  onOpenDiagnostics?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeRole,
  onSelectRole,
  health,
  onOpenAssistant,
  onOpenLogin,
  onOpenDiagnostics,
}) => {
  const { user, logout } = useAuth();
  const [showProfileMenu, setShowProfileMenu] = useState(false);

  const handleLogout = () => {
    logout();
    onSelectRole('landing');
    setShowProfileMenu(false);
  };

  return (
    <header className="border-b border-slate-800/80 bg-slate-900/90 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo & Clean Product Identity */}
        <div 
          onClick={() => {
            if (!user) {
              onSelectRole('landing');
            } else if (user.role === 'employer') {
              onSelectRole('employer');
            } else {
              onSelectRole('inspector');
            }
          }}
          className="flex items-center gap-3 cursor-pointer select-none group"
        >
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-600 via-indigo-600 to-cyan-500 flex items-center justify-center shadow-md shadow-blue-500/20 group-hover:scale-105 transition">
            <ShieldCheck className="w-5 h-5 text-white" />
          </div>
          <div>
            <span className="font-extrabold text-base tracking-tight text-white block">
              ShramAI
            </span>
            <p className="text-[11px] text-slate-400 font-medium hidden sm:block">
              AI-Powered Labour Compliance & Inspection Intelligence
            </p>
          </div>
        </div>

        {/* Navigation Bar — Dynamically Rendered Strictly by Role */}
        <nav className="flex items-center gap-1">
          
          {/* Unauthenticated View: No internal portals visible */}
          {!user && (
            <div className="flex items-center gap-2 sm:gap-3">
              <button
                onClick={() => onOpenLogin('employer')}
                className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-amber-300 hover:text-amber-200 hover:bg-amber-500/10 border border-amber-500/30 transition flex items-center gap-1.5 cursor-pointer"
              >
                <Building2 className="w-3.5 h-3.5 text-amber-400" />
                <span>Employer Login</span>
              </button>

              <button
                onClick={() => onOpenLogin('inspector')}
                className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 shadow-md shadow-blue-500/20 transition flex items-center gap-1.5 cursor-pointer"
              >
                <FileSearch className="w-3.5 h-3.5" />
                <span>Inspector Login</span>
              </button>
            </div>
          )}

          {/* Employer Navigation: STRICTLY employer relevant features */}
          {user && user.role === 'employer' && (
            <div className="flex items-center gap-1 bg-slate-950/80 p-1 rounded-xl border border-slate-800/80">
              <button
                onClick={() => onSelectRole('employer')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                  activeRole === 'employer'
                    ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`}
              >
                Overview
              </button>

              <button
                onClick={() => onSelectRole('upload')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                  activeRole === 'upload'
                    ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`}
              >
                <UploadCloud className="w-3.5 h-3.5 text-amber-400" />
                <span>Documents</span>
              </button>

              <button
                onClick={() => onSelectRole('employer')}
                className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-400 hover:text-slate-200 hover:bg-slate-900/60 transition cursor-pointer"
              >
                <FileCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>Compliance</span>
              </button>

              <button
                onClick={onOpenAssistant}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-cyan-300 hover:text-cyan-200 hover:bg-cyan-500/10 transition cursor-pointer"
              >
                <Bot className="w-3.5 h-3.5 text-cyan-400" />
                <span className="hidden sm:inline">AI Assistant</span>
              </button>
            </div>
          )}

          {/* Inspector Navigation: STRICTLY inspector relevant features */}
          {user && (user.role === 'inspector' || user.role === 'admin') && (
            <div className="flex items-center gap-1 bg-slate-950/80 p-1 rounded-xl border border-slate-800/80">
              <button
                onClick={() => onSelectRole('inspector')}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                  activeRole === 'inspector'
                    ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`}
              >
                Overview
              </button>

              <button
                onClick={() => onSelectRole('inspector')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                  activeRole === 'inspector' || activeRole === 'establishment-detail'
                    ? 'bg-blue-600/20 text-blue-300 border border-blue-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60'
                }`}
              >
                <FileSearch className="w-3.5 h-3.5 text-blue-400" />
                <span>Inspection Queue</span>
              </button>

              <button
                onClick={onOpenAssistant}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold text-cyan-300 hover:text-cyan-200 hover:bg-cyan-500/10 transition cursor-pointer"
              >
                <Bot className="w-3.5 h-3.5 text-cyan-400" />
                <span className="hidden sm:inline">Labour AI</span>
              </button>
            </div>
          )}
        </nav>

        {/* Right Controls: User Profile & Logout */}
        <div className="flex items-center gap-2 sm:gap-3">
          
          {/* Health & Diagnostics indicator */}
          <button
            onClick={onOpenDiagnostics}
            title={`Open System Diagnostics & Statutory Coverage Telemetry (Status: ${health?.status || 'healthy'})`}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-950/80 hover:bg-emerald-500/10 border border-slate-800 hover:border-emerald-500/40 text-[11px] text-slate-300 hover:text-emerald-300 transition cursor-pointer group"
          >
            <span className={`w-2 h-2 rounded-full ${health?.status === 'offline' ? 'bg-rose-400' : 'bg-emerald-400'} group-hover:animate-ping`} />
            <Activity className="w-3.5 h-3.5 text-emerald-400" />
            <span className="font-semibold hidden sm:inline">Diagnostics</span>
            <span className="font-mono text-[10px] text-slate-400 hidden lg:inline">({health?.status || 'operational'})</span>
          </button>

          {/* Authenticated User Menu */}
          {user && (
            <div className="relative">
              <button
                onClick={() => setShowProfileMenu(!showProfileMenu)}
                className="flex items-center gap-2 pl-3 pr-2 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60 transition cursor-pointer"
              >
                <div className={`w-6 h-6 rounded-lg flex items-center justify-center text-xs font-bold ${
                  user.role === 'employer' ? 'bg-amber-500 text-slate-950' : 'bg-blue-600 text-white'
                }`}>
                  {user.name[0]}
                </div>
                <div className="text-left hidden md:block">
                  <p className="text-xs font-semibold text-white leading-tight">{user.name}</p>
                  <p className="text-[10px] text-slate-400 capitalize">{user.role}</p>
                </div>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
              </button>

              {/* Profile Dropdown */}
              {showProfileMenu && (
                <div className="absolute right-0 mt-2 w-64 glass-panel rounded-2xl border border-slate-800 shadow-2xl p-3 space-y-3 z-50 bg-slate-900">
                  <div className="space-y-1 pb-2 border-b border-slate-800">
                    <p className="text-xs font-bold text-white">{user.name}</p>
                    <p className="text-[11px] text-slate-400 font-mono">{user.email}</p>
                    <span className={`inline-block text-[10px] font-mono px-2 py-0.5 rounded uppercase font-semibold ${
                      user.role === 'employer' 
                        ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30' 
                        : 'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                    }`}>
                      {user.designation}
                    </span>
                    {user.establishment_id && (
                      <p className="text-[10px] text-slate-400 mt-1">
                        Establishment: <strong className="text-amber-400 font-mono">{user.establishment_id}</strong>
                      </p>
                    )}
                    {user.jurisdiction && (
                      <p className="text-[10px] text-slate-400 mt-1">
                        Jurisdiction: <strong className="text-blue-400">{user.jurisdiction}</strong>
                      </p>
                    )}
                  </div>

                  <button
                    onClick={handleLogout}
                    className="w-full flex items-center justify-between p-2 rounded-xl text-rose-400 hover:bg-rose-500/10 text-xs font-semibold transition cursor-pointer"
                  >
                    <span>Sign Out & Lock Session</span>
                    <LogOut className="w-3.5 h-3.5" />
                  </button>
                </div>
              )}
            </div>
          )}

        </div>

      </div>
    </header>
  );
};
