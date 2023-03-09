import { createClient } from '@supabase/supabase-js'

// Create a single supabase client for interacting with your database
export const supabase = createClient('https://app.supabase.com/new/fhkcwccnpsfemtkedhfo', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVzcnhxc2RhZG9meXpydmhma2JvIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzgzMjIyNDYsImV4cCI6MTk5Mzg5ODI0Nn0.bOAav70OfdZlDxLn2ZPpGzZjfzyyE4zVmA-4_ldpSok')

