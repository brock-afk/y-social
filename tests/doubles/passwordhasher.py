from y_social.user.interface import PasswordHasher


class PasswordHasherTestDouble(PasswordHasher):
    def hash(self, password: str) -> str:
        return password + "hashed"

    def verify(self, password: str, hashed_password: str) -> bool:
        return password + "hashed" == hashed_password
