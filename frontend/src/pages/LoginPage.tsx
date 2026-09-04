import React, { useState, useEffect } from 'react';
import { ShieldCheck, Lock, Building2, FileSearch, ArrowRight, AlertCircle, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Role } from '../types';
import { API_BASE } from '../config/api';

interface LoginPageProps {
  initialRole?: 'employer' | 'inspector';
  onSuccess: (role: 'employer' | 'inspector') => void;
  onCancel?: () => void;
}

export const LoginPage: React.FC<LoginPageProps> = ({ 
  initialRole = 'employer', 
  onSuccess,
  onCancel,
}) => {
  const { login } = useAuth();
  const [selectedRole, setSelectedRole] = useState<'employer' | 'inspector'>(initialRole);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Sync role credentials when switching role tab or opening
  useEffect(() => {
    if (selectedRole === 'employer') {
      setEmail('employer@abcindustries.com');
      setPassword('Employer@123');
    } else {
      setEmail('inspector@shram.gov.in');
      setPassword('Inspector@123');
    }
    setError('');
  }, [selectedRole]);

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_BASE}/auth/login/json`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Authentication failed. Please verify credentials.');
      }

      const data = await response.json();

      // Strict backend role verification
      const userRole = data.role as Role;
      if (selectedRole === 'employer' && userRole !== 'employer') {
        throw new Error('Access Restricted — Your account is not an Employer account.');
      }
      if (selectedRole === 'inspector' && userRole !== 'inspector' && userRole !== 'admin') {
        throw new Error('Access Restricted — Your account does not have Inspector permissions.');
      }

      login(data.email, userRole, data.name, data.access_token);
      onSuccess(selectedRole);
    } catch (err: any) {
      setError(err.message || 'Authentication error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const isEmployer = selectedRole === 'employer';

  return (
    <div className="w-full max-w-md mx-auto glass-panel p-6 sm:p-8 rounded-3xl border border-slate-800 space-y-6 shadow-2xl bg-slate-900/95 backdrop-blur-xl">
      
      {/* Brand Header */}
      <div className="text-center space-y-2">
        <div className={`w-14 h-14 rounded-2xl mx-auto flex items-center justify-center shadow-lg transition ${
          isEmployer 
            ? 'bg-gradient-to-br from-amber-500 to-amber-700 shadow-amber-500/20 text-slate-950' 
            : 'bg-gradient-to-br from-blue-600 to-indigo-600 shadow-blue-500/20 text-white'
        }`}>
          {isEmployer ? <Building2 className="w-7 h-7" /> : <ShieldCheck className="w-7 h-7" />}
        </div>
        <h1 className="text-xl font-extrabold text-white">
          {isEmployer ? 'Employer Portal Login' : 'Labour Inspector Login'}
        </h1>
        <p className="text-xs text-slate-400 max-w-xs mx-auto">
          {isEmployer 
            ? 'Access your establishment compliance filings, self-audits, and corrective actions.'
            : 'Access statutory risk intelligence, priority inspection queues, and field dockets.'
          }
        </p>
      </div>

      {/* Role Selection Tabs */}
      <div className="grid grid-cols-2 p-1 rounded-xl bg-slate-950/80 border border-slate-800">
        <button
          type="button"
          onClick={() => setSelectedRole('employer')}
          className={`py-2 px-3 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer ${
            isEmployer 
              ? 'bg-amber-500 text-slate-950 shadow-md font-bold' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Building2 className="w-3.5 h-3.5" />
          <span>Employer</span>
        </button>

        <button
          type="button"
          onClick={() => setSelectedRole('inspector')}
          className={`py-2 px-3 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition cursor-pointer ${
            !isEmployer 
              ? 'bg-blue-600 text-white shadow-md font-bold' 
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <FileSearch className="w-3.5 h-3.5" />
          <span>Inspector</span>
        </button>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs flex items-start gap-2 animate-shake">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
          <span>{error}</span>
        </div>
      )}

      {/* Login Form */}
      <form onSubmit={handleLoginSubmit} className="space-y-4">
        <div className="space-y-1.5">
          <label className="text-xs font-semibold text-slate-300">
            {isEmployer ? 'Establishment Email' : 'Official Government Email'}
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 text-xs focus:outline-none focus:border-cyan-500 transition font-mono"
            placeholder={isEmployer ? 'employer@abcindustries.com' : 'inspector@shram.gov.in'}
          />
        </div>

        <div className="space-y-1.5">
          <label className="text-xs font-semibold text-slate-300">
            Password
          </label>
          <div className="relative">
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950 border border-slate-800 text-slate-100 text-xs focus:outline-none focus:border-cyan-500 transition font-mono pr-9"
              placeholder="••••••••"
            />
            <Lock className="w-4 h-4 text-slate-500 absolute right-3 top-3 pointer-events-none" />
          </div>
        </div>

        {/* Demo Credentials Reminder Note */}
        <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 text-[11px] text-slate-400 space-y-1">
          <div className="flex items-center justify-between text-slate-300 font-semibold">
            <span>Demo Profile:</span>
            <span className="font-mono text-[10px] text-cyan-400">
              {isEmployer ? 'EST-001 (ABC Industries Ltd.)' : 'Central Enforcement Officer'}
            </span>
          </div>
          <p className="text-[10px] text-slate-400">
            Credentials auto-populated for verification. Click Sign In to authenticate.
          </p>
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-3 rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition shadow-lg cursor-pointer disabled:opacity-50 ${
            isEmployer
              ? 'bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 shadow-amber-500/20'
              : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white shadow-blue-500/25'
          }`}
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Authenticating...</span>
            </>
          ) : (
            <>
              <span>Sign In to {isEmployer ? 'Employer Portal' : 'Inspector Portal'}</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>

        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="w-full py-2 text-xs text-slate-400 hover:text-slate-200 transition cursor-pointer"
          >
            Cancel & Return to Launch Page
          </button>
        )}
      </form>
    </div>
  );
};
