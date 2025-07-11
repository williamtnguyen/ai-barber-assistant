import { MessageCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { Link } from 'react-router-dom';

interface NavigationProps {
  currentPath: string;
  isMobile?: boolean;
  onClose?: () => void;
}

const navigationItems = [
  { path: '/chat', label: 'Chat', icon: MessageCircle },
];

export function Navigation({ currentPath, isMobile = false, onClose }: NavigationProps) {
  const handleClick = () => {
    if (isMobile && onClose) {
      onClose();
    }
  };

  return (
    <nav className={cn(
      "bg-white border-r border-gray-200",
      isMobile ? "w-full" : "fixed left-0 top-0 w-64 h-screen overflow-y-auto z-40"
    )}>
      <div className="p-4 space-y-2">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentPath === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              onClick={handleClick}
              className="block"
            >
              <Button
                variant={isActive ? "default" : "ghost"}
                className={cn(
                  "w-full justify-start",
                  isActive && "bg-purple-600 hover:bg-purple-700"
                )}
              >
                <Icon className="mr-2 h-4 w-4" />
                {item.label}
              </Button>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
