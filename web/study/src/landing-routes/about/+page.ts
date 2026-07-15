import { redirect } from '@sveltejs/kit';
import type { Load } from '@sveltejs/kit';

export const load: Load = ({ url }) => {
	throw redirect(308, `/${url.search}`);
};
