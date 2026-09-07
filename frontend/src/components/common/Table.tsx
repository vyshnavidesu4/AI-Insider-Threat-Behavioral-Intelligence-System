import React from 'react';
import { clsx } from 'clsx';

export interface Column<T> {
  header: string;
  accessor?: keyof T | ((row: T) => React.ReactNode);
  className?: string;
  headerClassName?: string;
  width?: string;
}

interface TableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (row: T, index: number) => string;
  onRowClick?: (row: T) => void;
  emptyMessage?: string;
  isLoading?: boolean;
}

export function DenseTable<T>({
  columns,
  data,
  keyExtractor,
  onRowClick,
  emptyMessage = 'No telemetry or events recorded in this window.',
  isLoading = false,
}: TableProps<T>) {
  if (isLoading) {
    return (
      <div className="p-8 text-center text-xs font-mono-dense text-socText-muted bg-soc-panel border border-soc-border">
        [POLLING SOC INGESTION PIPELINE...]
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="p-8 text-center text-xs font-mono-dense text-socText-muted bg-soc-panel border border-soc-border">
        {emptyMessage}
      </div>
    );
  }

  return (
    <div className="w-full overflow-x-auto border border-soc-border bg-soc-panel shadow-soc-table">
      <table className="soc-table">
        <thead>
          <tr>
            {columns.map((col, idx) => (
              <th
                key={idx}
                className={clsx('soc-th', col.headerClassName)}
                style={col.width ? { width: col.width } : undefined}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-soc-borderMuted">
          {data.map((row, rowIdx) => (
            <tr
              key={keyExtractor(row, rowIdx)}
              onClick={() => onRowClick && onRowClick(row)}
              className={clsx(
                'soc-tr-hover transition-colors',
                rowIdx % 2 === 1 && 'bg-soc-bg/40',
                onRowClick && 'cursor-pointer'
              )}
            >
              {columns.map((col, colIdx) => (
                <td key={colIdx} className={clsx('soc-td', col.className)}>
                  {typeof col.accessor === 'function'
                    ? col.accessor(row)
                    : col.accessor
                    ? (row[col.accessor] as unknown as React.ReactNode)
                    : null}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
