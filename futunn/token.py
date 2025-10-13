"""
Token Manager for Futunn API

Handles acquisition and management of authentication tokens required for API requests.
Inspired by TokenAcquirer from py-googletrans.
"""

import logging
import re
from typing import Optional, Dict
import httpx

from futunn import urls, constants
from futunn.exceptions import TokenExpiredError

logger = logging.getLogger(__name__)


class TokenManager:
    """
    Manages authentication tokens for Futunn API.

    Fetches and caches tokens from cookies and headers when visiting the main page.
    """

    def __init__(self, client: httpx.AsyncClient):
        """
        Initialize TokenManager

        Args:
            client: httpx.AsyncClient instance to use for requests
        """
        self.client = client
        self.csrf_token: Optional[str] = None
        self.quote_token: Optional[str] = None
        self._headers_cache: Optional[Dict[str, str]] = None

    async def get_tokens(self) -> Dict[str, str]:
        """
        Get authentication tokens, fetching new ones if necessary.

        Returns:
            Dict containing required headers with tokens

        Raises:
            TokenExpiredError: If unable to fetch tokens
        """
        if self.csrf_token is None or self.quote_token is None:
            await self._fetch_tokens()

        return self._build_headers()

    async def _fetch_tokens(self) -> None:
        """
        Fetch tokens by visiting the main Futunn page.

        This mimics a browser visit to extract cookies and tokens.
        """
        try:
            logger.info("Fetching authentication tokens from Futunn")

            # Visit the main stock list page to get cookies
            response = await self.client.get(
                urls.STOCK_LIST_PAGE,
                headers={
                    "User-Agent": constants.DEFAULT_USER_AGENT,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                },
                follow_redirects=True,
            )

            if response.status_code != 200:
                raise TokenExpiredError(
                    f"Failed to fetch tokens: HTTP {response.status_code}"
                )

            # Extract tokens from cookies
            cookies = response.cookies
            self.csrf_token = self._extract_csrf_token(response, cookies)
            self.quote_token = self._extract_quote_token(response, cookies)

            logger.info(
                f"Successfully fetched tokens: csrf={bool(self.csrf_token)}, "
                f"quote={bool(self.quote_token)}"
            )

        except httpx.RequestError as e:
            logger.error(f"Network error while fetching tokens: {e}")
            raise TokenExpiredError(f"Network error: {e}")

    def _extract_csrf_token(
        self, response: httpx.Response, cookies: httpx.Cookies
    ) -> str:
        """
        Extract CSRF token from response.

        Args:
            response: HTTP response object
            cookies: Cookies from response

        Returns:
            CSRF token string
        """
        # Try to find token in response headers
        csrf_token = response.headers.get("x-csrf-token")
        if csrf_token:
            return csrf_token

        # Try to find in page content
        content = response.text
        match = re.search(r'csrf[_-]?token["\']\s*[:=]\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)

        # Fallback: generate a simple token (this might need adjustment based on actual requirements)
        logger.warning("Could not extract CSRF token, using fallback")
        return "iwtmChEzi0ixw18P983l5ai7"  # From observed network traffic

    def _extract_quote_token(
        self, response: httpx.Response, cookies: httpx.Cookies
    ) -> str:
        """
        Extract quote token from response.

        Args:
            response: HTTP response object
            cookies: Cookies from response

        Returns:
            Quote token string
        """
        # Try to find in response content
        content = response.text
        match = re.search(r'quote[_-]?token["\']\s*[:=]\s*["\']([^"\']+)["\']', content)
        if match:
            return match.group(1)

        # Fallback: generate a simple token
        logger.warning("Could not extract quote token, using fallback")
        return "99227e34c9"  # From observed network traffic

    def _build_headers(self) -> Dict[str, str]:
        """
        Build request headers with authentication tokens.

        Returns:
            Dictionary of headers
        """
        return {
            "futu-x-csrf-token": self.csrf_token or "",
            "quote-token": self.quote_token or "",
            "referer": urls.STOCK_LIST_PAGE,
            "user-agent": constants.DEFAULT_USER_AGENT,
            "accept": "application/json, text/plain, */*",
        }

    async def refresh_tokens(self) -> Dict[str, str]:
        """
        Force refresh of authentication tokens.

        Returns:
            Dict containing refreshed headers with tokens
        """
        logger.info("Refreshing authentication tokens")
        self.csrf_token = None
        self.quote_token = None
        return await self.get_tokens()

    def invalidate(self) -> None:
        """Invalidate cached tokens, forcing refresh on next request"""
        logger.info("Invalidating cached tokens")
        self.csrf_token = None
        self.quote_token = None
        self._headers_cache = None
