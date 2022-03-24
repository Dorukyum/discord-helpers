import discord


class Webhooks:
    @classmethod
    async def find_and_send(
        cls,
        text: str,
        *,
        channel: discord.TextChannel,
        webhook_name: str,
        sender_name: str = None,
        icon_url: str = None
    ) -> discord.WebhookMessage:
        webhooks = await channel.webhooks()
        for webhook in webhooks:
            if webhook.name == webhook_name:
                return await cls.send_message(
                    text, webhook, sender_name=sender_name, icon_url=icon_url
                )
        else:
            raise RuntimeError("No webhook was found named {}".format(webhook_name))

    @classmethod
    async def send_message(
        cls,
        text: str,
        webhook: discord.Webhook,
        *,
        sender_name: str = None,
        icon_url: str = None
    ) -> discord.WebhookMessage:
        if not icon_url:
            icon_url = webhook.avatar
        if not sender_name:
            sender_name = webhook.name
        return await webhook.send(text, username=sender_name, avatar_url=icon_url)
