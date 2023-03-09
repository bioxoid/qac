import { supabase } from "$lib/supabaseClient";

export async function load({getClientAddress}) {
  const { data } = await supabase.from("Constellation").select();
  return {
    countries: data ?? [],
    ip: getClientAddress(),
  };
}