import React from 'react';

/**
 * A reusable, professional shimmer skeleton for loading states.
 */
export const Skeleton = ({ className }) => (
  <div className={`animate-pulse bg-white/5 rounded-lg ${className}`} />
);

export const BookCardSkeleton = () => (
  <div className="glass-card overflow-hidden h-[400px] flex flex-col space-y-4 p-4">
    <Skeleton className="h-48 w-full" />
    <Skeleton className="h-6 w-3/4" />
    <Skeleton className="h-4 w-1/2" />
    <div className="mt-auto flex justify-between">
      <Skeleton className="h-8 w-1/3" />
      <Skeleton className="h-8 w-1/4" />
    </div>
  </div>
);

export const DetailSkeleton = () => (
  <div className="grid grid-cols-1 md:grid-cols-3 gap-12 animate-pulse">
    <div className="md:col-span-1">
      <Skeleton className="h-[450px] w-full rounded-2xl" />
    </div>
    <div className="md:col-span-2 space-y-8">
      <div className="space-y-4">
        <Skeleton className="h-12 w-3/4" />
        <Skeleton className="h-6 w-1/4" />
        <div className="flex gap-3">
          <Skeleton className="h-8 w-20 rounded-full" />
          <Skeleton className="h-8 w-20 rounded-full" />
        </div>
      </div>
      <Skeleton className="h-32 w-full" />
      <Skeleton className="h-24 w-full" />
    </div>
  </div>
);
