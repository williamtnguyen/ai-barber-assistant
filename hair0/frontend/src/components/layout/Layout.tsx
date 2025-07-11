import { useState } from 'react';
import { Header } from './Header';
import { Navigation } from './Navigation';
import { cn } from '@/lib/utils';

interface LayoutProps {
  children: React.ReactNode;
  currentPath: string;
}

export function Layout({ children, currentPath }: LayoutProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const closeMobileMenu = () => {
    setIsMobileMenuOpen(false);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        onMenuToggle={toggleMobileMenu}
        isMobileMenuOpen={isMobileMenuOpen}
      />
      
      <div className="flex">
        {/* Desktop Navigation */}
        <div className="hidden md:block">
          <Navigation 
            currentPath={currentPath}
          />
        </div>
        
        {/* Mobile Navigation Overlay */}
        {isMobileMenuOpen && (
          <div className="fixed inset-0 z-50 md:hidden">
            <div 
              className="absolute inset-0 bg-black bg-opacity-50"
              onClick={closeMobileMenu}
            />
            <div className="absolute left-0 top-0 h-full w-64 bg-white">
              <Navigation 
                currentPath={currentPath}
                isMobile={true}
                onClose={closeMobileMenu}
              />
            </div>
          </div>
        )}
        
        {/* Main Content */}
        <main className={cn(
          "flex-1 p-6",
          "md:ml-64" // Add left margin equal to sidebar width (w-64 = 256px)
        )}>
          {children}
        </main>
      </div>
    </div>
  );
}
