import { GET, POST, type Fetcher } from '../utils';
import type { SessionState } from '../types';
import type { GenericStatus } from '../utils/types';

/**
 * Get the current user.
 */
export const me = async (f: Fetcher) => {
	return await GET<never, SessionState>(f, 'me');
};

/**
 * Request for logging in via magic link sent to email.
 */
export type MagicLoginRequest = {
	email: string;
	forward: string;
};

/**
 * Request for login-as magic link sent to admin email.
 */
export type LoginAsRequest = {
	instructor_email: string;
	admin_email: string;
	forward: string;
};

/**
 * Perform a login sending a magic link.
 */
export const loginWithMagicLink = async (f: Fetcher, email: string, forward: string) => {
	const url = `login/magic`;
	const response = await POST<MagicLoginRequest, GenericStatus>(f, url, {
		email,
		forward
	});
	return response;
};

/**
 * Request a login-as magic link for admins.
 */
export const loginAsWithMagicLink = async (
	f: Fetcher,
	instructor_email: string,
	admin_email: string,
	forward: string
) => {
	const url = `admin/login-as`;
	const response = await POST<LoginAsRequest, GenericStatus>(f, url, {
		instructor_email,
		admin_email,
		forward
	});
	return response;
};

/**
 * Mark the profile moved notice as seen for this instructor.
 */
export const markNoticeSeen = async (f: Fetcher, key: string) => {
	const url = `me/notices/seen`;
	return await POST<{ key: string }, GenericStatus>(f, url, { key });
};
