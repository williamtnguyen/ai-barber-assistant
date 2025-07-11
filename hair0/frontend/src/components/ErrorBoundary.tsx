import { Component } from 'react';
import type { ErrorInfo, ReactNode } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
    errorInfo: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({
      error,
      errorInfo,
    });
  }

  private handleReload = () => {
    window.location.reload();
  };

  private handleGoHome = () => {
    window.location.href = '/';
  };

  private handleResetError = () => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
          <div className="max-w-2xl w-full">
            <Card className="border-red-200 bg-red-50">
              <CardHeader className="text-center">
                <div className="flex justify-center mb-4">
                  <AlertTriangle className="h-16 w-16 text-red-500" />
                </div>
                <CardTitle className="text-2xl text-red-800">
                  Oops! Something went wrong
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="text-center">
                  <p className="text-red-700 mb-4">
                    The application encountered an unexpected error. Don't worry, this has been logged and we'll look into it.
                  </p>
                  
                  <div className="flex flex-col sm:flex-row gap-3 justify-center">
                    <Button onClick={this.handleReload} className="flex items-center">
                      <RefreshCw className="h-4 w-4 mr-2" />
                      Reload Page
                    </Button>
                    <Button onClick={this.handleGoHome} variant="outline" className="flex items-center">
                      <Home className="h-4 w-4 mr-2" />
                      Go Home
                    </Button>
                    <Button onClick={this.handleResetError} variant="ghost" className="flex items-center">
                      Try Again
                    </Button>
                  </div>
                </div>

                {process.env.NODE_ENV === 'development' && this.state.error && (
                  <details className="mt-6">
                    <summary className="cursor-pointer text-sm font-medium text-red-800 hover:text-red-900">
                      Show Error Details (Development Mode)
                    </summary>
                    <div className="mt-3 p-4 bg-red-100 rounded-lg border border-red-200">
                      <div className="mb-3">
                        <h4 className="font-medium text-red-800">Error:</h4>
                        <pre className="text-sm text-red-700 whitespace-pre-wrap break-words">
                          {this.state.error.toString()}
                        </pre>
                      </div>
                      
                      {this.state.errorInfo && (
                        <div>
                          <h4 className="font-medium text-red-800">Component Stack:</h4>
                          <pre className="text-xs text-red-600 whitespace-pre-wrap break-words max-h-40 overflow-y-auto">
                            {this.state.errorInfo.componentStack}
                          </pre>
                        </div>
                      )}
                    </div>
                  </details>
                )}

                <div className="text-center text-sm text-gray-600">
                  <p>
                    If this problem persists, please try refreshing the page or contact support.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}