import { useEffect, useState } from 'react';
import { Navbar } from './components/Navbar';
import { LandingPage } from './pages/LandingPage';
import { EmployerDashboard } from './pages/EmployerDashboard';
import { InspectorDashboard } from './pages/InspectorDashboard';
import { EstablishmentIntelligence } from './pages/EstablishmentIntelligence';
import { DocumentUploadView } from './pages/DocumentUploadView';
import { AIAssistantDrawer } from './pages/AIAssistantDrawer';
import { InspectionWorkflow } from './pages/InspectionWorkflow';
import { LoginPage } from './pages/LoginPage';
import { SystemDiagnosticsModal } from './components/SystemDiagnosticsModal';
import { AuthProvider, useAuth } from './context/AuthContext';
import { fetchHealth, fetchEstablishments, fetchEstablishmentDossier } from './services/api';
import { ActiveRole, SystemHealth, Establishment, EstablishmentDossier } from './types';
import { MOCK_DOSSIER } from './services/mockData';
import { Lock, ShieldAlert } from 'lucide-react';

function AppContent() {
  const { user } = useAuth();
  const [activeRole, setActiveRole] = useState<ActiveRole>(() => {
    const params = new URLSearchParams(window.location.search);
    const view = params.get('view');
    if (view === 'employer') return 'employer';
    if (view === 'inspector') return 'inspector';
    if (view === 'establishment-detail' || view === 'dossier') return 'establishment-detail';

    const saved = localStorage.getItem('shram_user');
    if (saved) {
      try {
        const u = JSON.parse(saved);
        return u.role === 'employer' ? 'employer' : 'inspector';
      } catch {
        return 'landing';
      }
    }
    return 'landing';
  });

  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [establishments, setEstablishments] = useState<Establishment[]>([]);
  const [selectedDossier, setSelectedDossier] = useState<EstablishmentDossier>(MOCK_DOSSIER);
  const [isAssistantOpen, setIsAssistantOpen] = useState(false);
  const [isDiagnosticsOpen, setIsDiagnosticsOpen] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(() => {
    const params = new URLSearchParams(window.location.search);
    return params.has('login');
  });
  const [loginTargetRole, setLoginTargetRole] = useState<'employer' | 'inspector'>(() => {
    const params = new URLSearchParams(window.location.search);
    return params.get('login') === 'inspector' ? 'inspector' : 'employer';
  });
  const [inspectionTarget, setInspectionTarget] = useState<{ id: string; name: string } | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const view = params.get('view');
    if (view === 'employer' && (!user || user.role !== 'employer')) {
      handleOpenLogin('employer');
    } else if ((view === 'inspector' || view === 'establishment-detail' || view === 'dossier') && (!user || user.role !== 'inspector')) {
      handleOpenLogin('inspector');
    }
  }, []);

  useEffect(() => {
    fetchHealth().then(setHealth);
    // Only fetch inspector queue establishments if user is inspector or admin
    if (user && (user.role === 'inspector' || user.role === 'admin')) {
      fetchEstablishments().then(setEstablishments);
    }
  }, [user]);

  const handleOpenLogin = (role: 'employer' | 'inspector') => {
    setLoginTargetRole(role);
    setShowLoginModal(true);
  };

  const handleLoginSuccess = (role: 'employer' | 'inspector') => {
    setShowLoginModal(false);
    setActiveRole(role);
    if (role === 'inspector') {
      fetchEstablishments().then(setEstablishments);
    }
  };

  const handleSelectEstablishment = async (establishmentId: string) => {
    const dossier = await fetchEstablishmentDossier(establishmentId);
    setSelectedDossier(dossier);
    setActiveRole('establishment-detail');
  };

  // RBAC Route Violations Detection
  const isInspectorDestination = activeRole === 'inspector' || activeRole === 'establishment-detail' || activeRole === 'inspection-workflow';
  const isEmployerDestination = activeRole === 'employer' || activeRole === 'upload';

  const isEmployerBlockedFromInspector = Boolean(user && user.role === 'employer' && isInspectorDestination);
  const isInspectorBlockedFromEmployer = Boolean(user && (user.role === 'inspector' || user.role === 'admin') && isEmployerDestination);
  const isUnauthenticatedBlocked = Boolean(!user && activeRole !== 'landing');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col selection:bg-cyan-500 selection:text-slate-950">
      
      {/* Top Navbar */}
      <Navbar
        activeRole={activeRole}
        onSelectRole={(role) => setActiveRole(role)}
        health={health}
        onOpenAssistant={() => setIsAssistantOpen(true)}
        onOpenLogin={handleOpenLogin}
        onOpenDiagnostics={() => setIsDiagnosticsOpen(true)}
      />

      {/* Main Routed Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Case 1: Unauthenticated user trying to access protected dashboards */}
        {isUnauthenticatedBlocked ? (
          <div className="max-w-md mx-auto my-14 glass-panel p-8 rounded-3xl border border-slate-800 text-center space-y-4 shadow-2xl">
            <div className="w-14 h-14 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 mx-auto">
              <Lock className="w-7 h-7" />
            </div>
            <div className="space-y-1">
              <h2 className="text-lg font-bold text-white">Authentication Required</h2>
              <p className="text-xs text-slate-400 leading-relaxed">
                Please sign in with your credentials to access protected compliance data.
              </p>
            </div>
            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
              <button
                onClick={() => handleOpenLogin('employer')}
                className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs transition cursor-pointer"
              >
                Employer Login
              </button>
              <button
                onClick={() => handleOpenLogin('inspector')}
                className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition cursor-pointer"
              >
                Inspector Login
              </button>
            </div>
          </div>
        ) : isEmployerBlockedFromInspector ? (
          /* Case 2: Employer trying to access Inspector routes */
          <div className="max-w-xl mx-auto my-14 glass-panel p-8 rounded-3xl border border-rose-500/30 text-center space-y-5 shadow-2xl">
            <div className="w-14 h-14 rounded-2xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400 mx-auto">
              <Lock className="w-7 h-7" />
            </div>
            <div className="space-y-1.5">
              <h2 className="text-lg font-bold text-white">Access Restricted</h2>
              <p className="text-xs text-slate-300 leading-relaxed">
                Your account does not have Inspector permissions.
              </p>
              <p className="text-[11px] text-slate-500">
                You are currently signed in as an Employer ({user?.name}). Statutory enforcement queues and inspector risk algorithms require authorized enforcement officer credentials.
              </p>
            </div>
            <div className="pt-2 flex items-center justify-center">
              <button
                onClick={() => setActiveRole('employer')}
                className="px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold transition cursor-pointer shadow-md shadow-amber-500/20"
              >
                Return to Employer Portal
              </button>
            </div>
          </div>
        ) : isInspectorBlockedFromEmployer ? (
          /* Case 3: Inspector trying to access Employer-only submission routes */
          <div className="max-w-xl mx-auto my-14 glass-panel p-8 rounded-3xl border border-blue-500/30 text-center space-y-5 shadow-2xl">
            <div className="w-14 h-14 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 mx-auto">
              <ShieldAlert className="w-7 h-7" />
            </div>
            <div className="space-y-1.5">
              <h2 className="text-lg font-bold text-white">Access Restricted</h2>
              <p className="text-xs text-slate-300 leading-relaxed">
                This portal is designated exclusively for registered Employers.
              </p>
              <p className="text-[11px] text-slate-500">
                You are currently signed in as an Enforcement Officer ({user?.name}). Use the Inspection Intelligence Queue for establishment audits.
              </p>
            </div>
            <div className="pt-2 flex items-center justify-center">
              <button
                onClick={() => setActiveRole('inspector')}
                className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition cursor-pointer shadow-md shadow-blue-500/20"
              >
                Return to Inspector Dashboard
              </button>
            </div>
          </div>
        ) : (
          /* Case 4: Authorized Views */
          <>
            {activeRole === 'landing' && (
              <LandingPage 
                onOpenLogin={handleOpenLogin}
                health={health} 
              />
            )}

            {activeRole === 'employer' && (
              <EmployerDashboard 
                onNavigate={(role) => setActiveRole(role)}
                onOpenAssistant={() => setIsAssistantOpen(true)}
              />
            )}

            {activeRole === 'inspector' && (
              <InspectorDashboard
                establishments={establishments}
                onSelectEstablishment={handleSelectEstablishment}
                onNavigate={(role) => setActiveRole(role)}
                onBeginInspection={(id: string, name: string) => {
                  setInspectionTarget({ id, name });
                  setActiveRole('inspection-workflow');
                }}
              />
            )}

            {activeRole === 'establishment-detail' && (
              <EstablishmentIntelligence
                dossier={selectedDossier}
                onBack={() => setActiveRole('inspector')}
                onNavigate={(role) => setActiveRole(role)}
                onBeginInspection={() => {
                  setInspectionTarget({ id: selectedDossier.establishment.id, name: selectedDossier.establishment.name });
                  setActiveRole('inspection-workflow');
                }}
              />
            )}

            {activeRole === 'inspection-workflow' && inspectionTarget && (
              <InspectionWorkflow
                establishmentId={inspectionTarget.id}
                establishmentName={inspectionTarget.name}
                onBack={() => setActiveRole('inspector')}
              />
            )}

            {activeRole === 'upload' && (
              <DocumentUploadView />
            )}
          </>
        )}
      </main>

      {/* Role-Specific Login Modal */}
      {showLoginModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
          <div className="relative w-full max-w-md">
            <LoginPage 
              initialRole={loginTargetRole}
              onSuccess={handleLoginSuccess}
              onCancel={() => setShowLoginModal(false)}
            />
          </div>
        </div>
      )}

      {/* AI Assistant Drawer */}
      <AIAssistantDrawer
        isOpen={isAssistantOpen}
        onClose={() => setIsAssistantOpen(false)}
      />

      {/* System Diagnostics & Statutory Coverage Telemetry Modal */}
      <SystemDiagnosticsModal
        isOpen={isDiagnosticsOpen}
        onClose={() => setIsDiagnosticsOpen(false)}
      />

      {/* Clean GovTech Product Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950 py-4 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-slate-500">
          <p>
            ShramAI • AI-Powered Labour Compliance & Inspection Intelligence
          </p>
          <p className="font-mono text-[11px] text-slate-600">
            Deterministic Statutory Validation • Calibrated Machine Learning • Evidence-Backed Audit
          </p>
        </div>
      </footer>
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
