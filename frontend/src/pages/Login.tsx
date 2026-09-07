import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, KeyRound, AlertCircle } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login, isLoggingIn } = useAuth();
  const [email, setEmail] = useState('analyst@regionalbank.com');
  const [password, setPassword] = useState('AnalystPassword123!');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    try {
      await login({ email, password });
      navigate('/');
    } catch (err: any) {
      setErrorMessage(
        err.response?.data?.detail || 'Authentication failed. Verify credentials with SOC Admin.'
      );
    }
  };

  return (
    <div className="min-h-screen bg-soc-bg flex items-center justify-center p-4">
      <div className="w-full max-w-sm bg-soc-panel border border-soc-border shadow-soc-panel rounded-sm">
        {/* Terminal Header */}
        <div className="px-4 py-3 bg-soc-subtle border-b border-soc-border flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4 text-emerald-500" />
            <span className="font-mono-dense text-xs font-bold text-slate-200 tracking-wider">
              SOC AUTHENTICATION GATEWAY
            </span>
          </div>
          <span className="text-2xs font-mono-dense text-socText-muted">[SEC-V1.0]</span>
        </div>

        {/* Content Form */}
        <form onSubmit={handleSubmit} className="p-4 space-y-3">
          <div className="text-2xs font-mono-dense text-socText-muted leading-relaxed pb-1 border-b border-soc-borderMuted">
            RESTRICTED SYSTEM // REGIONAL BANK INTERNAL AUDIT & BEHAVIORAL INTEL
          </div>

          {errorMessage && (
            <div className="flex items-center gap-2 p-2 bg-threat-criticalBg border border-threat-criticalBorder text-threat-criticalText text-2xs font-mono-dense rounded-sm">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          <div className="space-y-1">
            <label className="text-2xs font-mono-dense text-socText-secondary uppercase">
              Operator Identifier (Email)
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full bg-soc-bg border border-soc-border px-2.5 py-1.5 text-xs font-mono-dense text-slate-100 focus:outline-none focus:border-soc-borderFocus rounded-sm"
              placeholder="analyst@regionalbank.com"
            />
          </div>

          <div className="space-y-1">
            <label className="text-2xs font-mono-dense text-socText-secondary uppercase">
              Access Token / Credential
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full bg-soc-bg border border-soc-border px-2.5 py-1.5 text-xs font-mono-dense text-slate-100 focus:outline-none focus:border-soc-borderFocus rounded-sm"
              placeholder="••••••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={isLoggingIn}
            className="w-full mt-2 bg-soc-elevated hover:bg-slate-700 text-slate-100 border border-soc-border px-3 py-2 text-xs font-mono-dense font-bold uppercase tracking-wider flex items-center justify-center gap-2 rounded-sm transition-colors disabled:opacity-50"
          >
            <KeyRound className="w-3.5 h-3.5 text-emerald-400" />
            <span>{isLoggingIn ? 'AUTHENTICATING...' : 'INITIALIZE SESSION'}</span>
          </button>
        </form>

        <div className="px-4 py-2 bg-soc-bg/70 border-t border-soc-border text-2xs font-mono-dense text-socText-muted text-center">
          AUTHORIZED USE ONLY // ALL ACCESS LOGGED TO TAMPER-EVIDENT LEDGER
        </div>
      </div>
    </div>
  );
};
