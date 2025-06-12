'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { UserList } from '@/components/user-list';
import { UserForm } from '@/components/user-form';
import { Button } from '@/components/ui/button';
import { userApi } from '@/lib/api';
import { formatError } from '@/lib/utils';
import { User } from '@/types/user';
import { UserCreateFormData } from '@/lib/validations';
import { ArrowLeft } from 'lucide-react';

type View = 'list' | 'create' | 'edit';

export default function HomePage() {
  const [currentView, setCurrentView] = useState<View>('list');
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [error, setError] = useState<string | null>(null);
  const pageSize = 10;

  const queryClient = useQueryClient();

  // Fetch users with pagination
  const {
    data: usersData,
    isLoading,
    error: queryError,
    refetch,
  } = useQuery({
    queryKey: ['users', currentPage, pageSize],
    queryFn: () => userApi.getUsers({ page: currentPage, size: pageSize }),
  });

  // Create user mutation
  const createUserMutation = useMutation({
    mutationFn: userApi.createUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setCurrentView('list');
      setError(null);
    },
    onError: (error) => {
      setError(formatError(error));
    },
  });

  // Update user mutation
  const updateUserMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: UserCreateFormData }) =>
      userApi.updateUser(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setCurrentView('list');
      setSelectedUser(null);
      setError(null);
    },
    onError: (error) => {
      setError(formatError(error));
    },
  });

  // Delete user mutation
  const deleteUserMutation = useMutation({
    mutationFn: userApi.deleteUser,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      setError(null);
    },
    onError: (error) => {
      setError(formatError(error));
    },
  });

  const handleCreateUser = async (data: UserCreateFormData) => {
    await createUserMutation.mutateAsync(data);
  };

  const handleUpdateUser = async (data: UserCreateFormData) => {
    if (selectedUser) {
      await updateUserMutation.mutateAsync({ id: selectedUser.id, data });
    }
  };

  const handleDeleteUser = async (userId: string) => {
    await deleteUserMutation.mutateAsync(userId);
  };

  const handleEditUser = (user: User) => {
    setSelectedUser(user);
    setCurrentView('edit');
    setError(null);
  };

  const handleCreateNew = () => {
    setSelectedUser(null);
    setCurrentView('create');
    setError(null);
  };

  const handleBackToList = () => {
    setCurrentView('list');
    setSelectedUser(null);
    setError(null);
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const totalPages = usersData ? Math.ceil(usersData.total / pageSize) : 0;

  if (currentView === 'create') {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <Button variant="outline" onClick={handleBackToList}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Users
          </Button>
        </div>
        {error && (
          <div className="bg-destructive/15 text-destructive px-4 py-3 rounded-md">
            {error}
          </div>
        )}
        <UserForm
          onSubmit={handleCreateUser}
          isLoading={createUserMutation.isPending}
          title="Create New User"
          submitText="Create User"
        />
      </div>
    );
  }

  if (currentView === 'edit' && selectedUser) {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <Button variant="outline" onClick={handleBackToList}>
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Users
          </Button>
        </div>
        {error && (
          <div className="bg-destructive/15 text-destructive px-4 py-3 rounded-md">
            {error}
          </div>
        )}
        <UserForm
          user={selectedUser}
          onSubmit={handleUpdateUser}
          isLoading={updateUserMutation.isPending}
          title="Edit User"
          submitText="Update User"
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-destructive/15 text-destructive px-4 py-3 rounded-md">
          {error}
        </div>
      )}
      <UserList
        users={usersData?.users || []}
        isLoading={isLoading}
        error={queryError ? formatError(queryError) : null}
        onEdit={handleEditUser}
        onDelete={handleDeleteUser}
        onCreateNew={handleCreateNew}
        onRetry={refetch}
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={handlePageChange}
        total={usersData?.total || 0}
      />
    </div>
  );
}
