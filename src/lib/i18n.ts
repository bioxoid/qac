// src/i18n.js
import { browser } from '$app/environment'
import { register, init, getLocaleFromNavigator } from 'svelte-i18n';

register('en', () => import('../../static/en.json'));
register('ja', () => import('../../static/ja.json'));

const defaultLocale = 'ja'

init({
  fallbackLocale: 'ja',
	initialLocale: browser ? window.navigator.language : defaultLocale
});