import { Menu, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface HeaderProps {
  onMenuToggle: () => void;
  isMobileMenuOpen: boolean;
}

export function Header({ onMenuToggle, isMobileMenuOpen }: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between md:ml-64">
      <div className="flex items-center space-x-3 p-1">
        <h1 className="text-xl font-bold text-gray-900">AI Barber Assistant</h1>
      </div>
      
      <Button
        variant="ghost"
        size="sm"
        className="md:hidden"
        onClick={onMenuToggle}
      >
        {isMobileMenuOpen ? (
          <X className="h-5 w-5" />
        ) : (
          <Menu className="h-5 w-5" />
        )}
      </Button>
    </header>
  );
}
