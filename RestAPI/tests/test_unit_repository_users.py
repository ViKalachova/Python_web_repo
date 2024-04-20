import unittest
from unittest.mock import MagicMock, AsyncMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import User
from src.repository.users import get_user_by_email, create_user, update_token, confirmed_email, update_avatar
from src.schemas.user import UserSchema


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1, username='winner', email="winner@gmail.com", password='12345678', confirmed=False,
                         refresh_token=None)

    async def test_get_user_by_email(self):
        email = 'winner@gmail.com'
        mocked_user = MagicMock()
        mocked_user.scalar_one_or_none.return_value = self.user
        self.session.execute.return_value = mocked_user
        result = await get_user_by_email(email, self.session)
        self.assertEqual(result, self.user)

    @patch('src.repository.users.Gravatar', autospec=True)
    async def test_create_user(self, mock_gravatar):
        user_data = {"email": "test@example.com", "username": "test", "password": "password"}
        user_schema = UserSchema(**user_data)
        mock_gravatar_instance = MagicMock()
        mock_gravatar.return_value = mock_gravatar_instance
        mock_gravatar_instance.get_image.return_value = "https://example.com/avatar.jpg"
        self.session.commit.return_value = None
        self.session.refresh.return_value = User(**user_data)
        new_user = await create_user(user_schema, self.session)
        self.assertEqual(new_user.email, user_schema.email)
        self.assertEqual(new_user.username, user_schema.username)
        self.assertEqual(new_user.avatar, mock_gravatar_instance.get_image())
        self.session.commit.assert_awaited_once()

    async def test_update_token(self):
        new_token = "new_token"
        await update_token(self.user, new_token, self.session)
        self.assertEqual(self.user.refresh_token, new_token)

    @patch('src.repository.users.get_user_by_email')
    async def test_confirmed_email(self, mock_get_user_by_email):
        self.session.add(self.user)
        await self.session.commit()
        mock_get_user_by_email.return_value = self.user
        await confirmed_email(self.user.email, self.session)
        self.assertTrue(self.user.confirmed)

    @patch('src.repository.users.get_user_by_email')
    async def test_update_avatar(self, mock_get_user_by_email):
        self.session.add(self.user)
        await self.session.commit()
        mock_get_user_by_email.return_value = self.user
        new_avatar_url = "new_avatar_url"
        updated_user = await update_avatar(self.user.email, new_avatar_url, self.session)
        self.assertEqual(updated_user.avatar, new_avatar_url)
