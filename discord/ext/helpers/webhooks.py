import discord


class Webhooks:
	@staticmethod
	async def find_and_send(
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
				if not icon_url:
					icon_url = webhook.avatar
				if not sender_name:
					sender_name = webhook.name
				return await webhook.send(
					text, username=sender_name, avatar_url=icon_url
				)
		else:
			raise RuntimeError("No webhook was found named {}".format(webhook_name))

	@staticmethod
	async def send_message(
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
