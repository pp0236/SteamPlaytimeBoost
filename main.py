import steam.client, steam.core, steam.enums, threading, time
from goto import with_goto

cfg_gameid = [ 440 ] # [appid1, appid2, appid3, ...]
cfg_invisible = True

class thingThatMakeMultiThreadWorkWithSteamModule():
	done = False
	@with_goto
	def login(self, usr, pw):
		print("  steam account " + usr)
		_2fa = None
		_mail = None

		label .relog
		client = steam.client.SteamClient()
		result = client.login(usr, pw, auth_code=_mail, two_factor_code=_2fa)
		# AccountLoginDeniedNeedTwoFactor (mobile steamguard)
		if result == 85:
			label ._2faIn
			_2fa = input("  SteamGuard code: ")
			goto .relog
		# AccountLogonDenied (mail steamguard)
		elif result == 63:
			label .mailIn
			_mail = input("  SteamGuard code: ")
			goto .relog
		# TwoFactorCodeMismatch (mobile steamguard)
		elif result == 88:
			print("  SteamGuard code mismatch")
			time.sleep(3)
			goto ._2faIn
		# InvalidLoginAuthCode (mail steamguard)
		elif result == 65:
			print("  SteamGuard code mismatch")
			time.sleep(3)
			goto .mailIn
		# InvalidPassword
		elif result == 5:
			print("  Invaild password for account " + usr)
			self.done = True
			return

		if result == 1:
			print("  Logged in as user " + client.user.name)
			client.games_played(cfg_gameid)
			if cfg_invisible:
				client.change_status(persona_state=steam.enums.common.EPersonaState.Invisible)

			self.done = True

			client.run_forever()
		else:
			print("  error")
			print(result)
			self.done = True

def main():
	f = open("accounts.txt", "r")
	accounts = f.read().splitlines()
	f.close()

	for account in accounts:
		usr, pw = account.split(":")
		#print(usr, pw)
		obj = thingThatMakeMultiThreadWorkWithSteamModule()
		threading._start_new_thread(obj.login, (usr, pw, ))
		while not obj.done:
			time.sleep(0.5)
		

	#print("end")
	while 1:
		time.sleep(999999)

#https://github.com/ValvePython/steam/blob/b2e1f7755c8f65b20a27cb767e2acb4346002f99/steam/client/builtins/user.py#L121
#just add custom status
# nvm just dont
#def patchMethod(self, app_ids):
#	pass

#import steam.client.builtins.user
#steam.client.builtins.user.User.games_played = patchMethod


if __name__ == "__main__":
	main()