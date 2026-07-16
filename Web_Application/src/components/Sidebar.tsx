import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Beef, FileText, Settings, Bot } from 'lucide-react';
import { cn } from '@/lib/utils';

const navigation = [
  { name: 'Dashboard', to: '/', icon: LayoutDashboard },
  { name: 'Cows', to: '/cows', icon: Beef },
  { name: 'Reports', to: '/reports', icon: FileText },
  { name: 'AI Assistant', to: '/ai-assistant', icon: Bot },
  { name: 'Settings', to: '/settings', icon: Settings },
];

export const Sidebar = () => {
  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-border bg-card">
      <div className="flex h-16 items-center border-b border-border px-6">
        <div className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center overflow-hidden rounded-lg border border-border bg-white shadow-sm">
            <img src="/Gaurakshak_logo.jpeg" alt="Gaurakshak logo" className="h-full w-full object-cover" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-foreground">Gaurakshak</h1>
            <p className="text-xs text-muted-foreground">Monitoring Dashboard</p>
          </div>
        </div>
      </div>

      <nav className="space-y-1 p-4">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all',
                isActive
                  ? 'bg-primary text-primary-foreground shadow-md'
                  : 'text-muted-foreground hover:bg-muted hover:text-foreground'
              )
            }
          >
            <item.icon className="h-5 w-5" />
            {item.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};
