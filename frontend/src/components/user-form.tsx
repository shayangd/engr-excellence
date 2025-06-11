'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Loading } from '@/components/ui/loading';
import { userCreateSchema, UserCreateFormData } from '@/lib/validations';
import { User } from '@/types/user';

interface UserFormProps {
  user?: User;
  onSubmit: (data: UserCreateFormData) => Promise<void>;
  isLoading?: boolean;
  title: string;
  submitText: string;
}

export function UserForm({ user, onSubmit, isLoading, title, submitText }: UserFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<UserCreateFormData>({
    resolver: zodResolver(userCreateSchema),
    defaultValues: {
      name: user?.name || '',
      email: user?.email || '',
    },
  });

  const onFormSubmit = async (data: UserCreateFormData) => {
    try {
      await onSubmit(data);
      if (!user) {
        reset(); // Reset form only for create mode
      }
    } catch (error) {
      // Error handling is done in the parent component
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="name" className="text-sm font-medium">
              Name
            </label>
            <Input
              id="name"
              type="text"
              placeholder="Enter full name"
              {...register('name')}
              disabled={isLoading}
            />
            {errors.name && (
              <p className="text-sm text-destructive">{errors.name.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium">
              Email
            </label>
            <Input
              id="email"
              type="email"
              placeholder="Enter email address"
              {...register('email')}
              disabled={isLoading}
            />
            {errors.email && (
              <p className="text-sm text-destructive">{errors.email.message}</p>
            )}
          </div>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? (
              <>
                <Loading size="sm" className="mr-2" />
                {submitText}...
              </>
            ) : (
              submitText
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
