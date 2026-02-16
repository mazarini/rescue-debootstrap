from pydantic import BaseModel, Field, computed_field


class Host(BaseModel):
    hostname: str = Field(..., min_length=1)
    rescue_name: str = Field(..., min_length=1)
    domain: str = Field(default="localdomain")
    efi: bool = Field(default=True)
    mountpoint: str = Field(
        default="/mnt",
        pattern=r"^/mnt$|^/mnt/[^/]+(/[^/]+)*$",
        description=(
            "Valide : /mnt, /mnt/data, /mnt/rescue/boot\n"
            "Invalide : /mnt/, /mnt//data, /media, /mnt "
        ),
    )

    @computed_field(return_type=str, description="Nom complet : hostname.domain")
    @property
    def full_name(self) -> str:
        return f"{self.hostname}.{self.domain}"
