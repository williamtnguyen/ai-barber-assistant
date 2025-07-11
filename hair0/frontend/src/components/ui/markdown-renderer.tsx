import { useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeHighlight from 'rehype-highlight';

interface MarkdownRendererProps {
  content: string;
  isStreaming?: boolean;
}

// Function to detect if content contains markdown patterns
const hasMarkdownPatterns = (text: string): boolean => {
  const markdownPatterns = [
    /^#{1,6}\s+/m,           // Headers
    /\*\*.*?\*\*/,           // Bold
    /\*.*?\*/,               // Italic
    /`.*?`/,                 // Inline code
    /```[\s\S]*?```/,        // Code blocks
    /^\s*[-*+]\s+/m,         // Unordered lists
    /^\s*\d+\.\s+/m,         // Ordered lists
    /\[.*?\]\(.*?\)/,        // Links
    /^\s*>\s+/m,             // Blockquotes
    /^\s*\|.*\|.*\|/m,       // Tables
    /^---+$/m,               // Horizontal rules
  ];
  
  return markdownPatterns.some(pattern => pattern.test(text));
};

// Function to handle incomplete markdown during streaming
const preprocessStreamingMarkdown = (content: string, isStreaming: boolean): string => {
  if (!isStreaming) return content;
  
  // Handle incomplete code blocks
  const codeBlockMatches = content.match(/```[\s\S]*$/);
  if (codeBlockMatches && !content.endsWith('```')) {
    // If we have an incomplete code block, add a temporary closing
    return content + '\n```';
  }
  
  // Handle incomplete inline code
  const inlineCodeMatches = content.match(/`[^`]*$/);
  if (inlineCodeMatches) {
    // If we have an incomplete inline code, add a temporary closing
    return content + '`';
  }
  
  return content;
};

export function MarkdownRenderer({ content, isStreaming = false }: MarkdownRendererProps) {
  const { shouldRenderAsMarkdown, processedContent } = useMemo(() => {
    const shouldRender = hasMarkdownPatterns(content);
    const processed = shouldRender ? preprocessStreamingMarkdown(content, isStreaming) : content;
    
    return {
      shouldRenderAsMarkdown: shouldRender,
      processedContent: processed
    };
  }, [content, isStreaming]);

  if (!shouldRenderAsMarkdown) {
    // Render as plain text with preserved whitespace
    return <p className="whitespace-pre-wrap">{content}</p>;
  }

  return (
    <div>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          // Custom styling for paragraphs to preserve original spacing
          p: ({ children }) => (
            <p className="whitespace-pre-wrap mb-4 last:mb-0">
              {children}
            </p>
          ),
          // Custom styling for code blocks
          code: ({ className, children, ...props }) => {
            const isInline = !className?.includes('language-');
            return isInline ? (
              <code className="bg-gray-100 px-1 py-0.5 rounded text-sm" {...props}>
                {children}
              </code>
            ) : (
              <pre className="bg-gray-100 rounded-md p-3 overflow-x-auto my-4">
                <code className={className} {...props}>
                  {children}
                </code>
              </pre>
            );
          },
          // Custom styling for headers
          h1: ({ children }) => (
            <h1 className="text-2xl font-bold mb-4 mt-6 first:mt-0">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-xl font-bold mb-3 mt-5 first:mt-0">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-lg font-bold mb-2 mt-4 first:mt-0">
              {children}
            </h3>
          ),
          h4: ({ children }) => (
            <h4 className="text-base font-bold mb-2 mt-3 first:mt-0">
              {children}
            </h4>
          ),
          h5: ({ children }) => (
            <h5 className="text-sm font-bold mb-2 mt-3 first:mt-0">
              {children}
            </h5>
          ),
          h6: ({ children }) => (
            <h6 className="text-xs font-bold mb-2 mt-3 first:mt-0">
              {children}
            </h6>
          ),
          // Custom styling for lists
          ul: ({ children }) => (
            <ul className="list-disc list-inside mb-4 space-y-1">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-inside mb-4 space-y-1">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="whitespace-pre-wrap">
              {children}
            </li>
          ),
          // Custom styling for blockquotes
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-blue-500 pl-4 italic text-gray-700 my-4 whitespace-pre-wrap">
              {children}
            </blockquote>
          ),
          // Custom styling for tables
          table: ({ children }) => (
            <div className="overflow-x-auto my-4">
              <table className="min-w-full border-collapse border border-gray-300">
                {children}
              </table>
            </div>
          ),
          th: ({ children }) => (
            <th className="border border-gray-300 px-4 py-2 bg-gray-100 font-semibold text-left">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border border-gray-300 px-4 py-2">
              {children}
            </td>
          ),
          // Custom styling for links
          a: ({ href, children }) => (
            <a 
              href={href} 
              className="text-blue-600 hover:text-blue-800 underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              {children}
            </a>
          ),
          // Custom styling for horizontal rules
          hr: () => (
            <hr className="border-t border-gray-300 my-6" />
          ),
          // Custom styling for emphasis
          strong: ({ children }) => (
            <strong className="font-bold">
              {children}
            </strong>
          ),
          em: ({ children }) => (
            <em className="italic">
              {children}
            </em>
          ),
        }}
      >
        {processedContent}
      </ReactMarkdown>
    </div>
  );
}