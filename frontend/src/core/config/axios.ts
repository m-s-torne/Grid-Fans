import axios from 'axios'
import { supabase } from '@/core/config/supabase'
import { ENV } from '../services/env'

export const http = axios.create({
    baseURL: ENV.API_URL,
    headers: {
        accept: 'application/json',
    },
});

http.interceptors.request.use(async (config) => {
    const { data } = await supabase.auth.getSession();
    const token = data.session?.access_token;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

http.interceptors.response.use(
    (r) => r,
    (err) => {
        const status = err?.response?.status;
        const url = (err?.config?.baseURL ||"") + (err?.config?.url ||"");
        const params = err?.config?.params;
        const method = err?.config?.method;
        const hasAuth = !!err?.config?.headers?.Authorization;
        const data = err?.response?.data;

        console.error("API ERROR", { status, method, url, params, hasAuth, data });
        return Promise.reject(err);
    }
);
