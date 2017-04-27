using System;
using System.Text;
using System.Net;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

using Discord;
using Discord.Commands;

namespace Discord_Bot
{
	class MyBot
	{
		DiscordClient discord;
		CommandService commands;

		Random random;

		WebClient client = new WebClient();

		bool set = false;


		public MyBot()
		{
			#region Importand Stuff
			discord = new DiscordClient(x => {
				x.LogLevel = LogSeverity.Info;
				x.LogHandler = Log;
				
			});

			discord.UsingCommands(x => {
				x.PrefixChar = '!';
				x.AllowMentionPrefix = true;
			});
			#endregion

			//OHGJ_CreateTimeCommand("time");
			//OHGJ_CreateThemeCommand("theme");

			GetJamInfo();

			#region Commands
			random = new Random();
			commands = discord.GetService<CommandService>();


			INIT("set");
			#endregion

			

			#region More Importand Stuff
			discord.ExecuteAndWait(async () => {
				await discord.Connect("MzA3MjAxMDIwNzQ2NzkyOTcx.C-PCmQ.SwBizq971xb0uJTKN4Jq5nezAqg", TokenType.Bot);
			});
			#endregion
		}

		private void Log(object sender, LogMessageEventArgs e)
		{
			Console.WriteLine(e.Message);
		}



		#region Other Commands
		private void CreateTextCommand(string command, string response)
		{
			commands.CreateCommand(command).Do(async e =>
			{
				await e.Channel.SendMessage(response);
			});
		}	

		private void CreateImageCommand(string command, string[] imgs)
		{
			commands.CreateCommand(command).Do
				(
					async (e) => {
						int imgIndex = random.Next(imgs.Length);
						string img = imgs[imgIndex];
						await e.Channel.SendFile(img);
					});
		}

		private void INIT(string command)
		{
			commands.CreateCommand(command).Do(
				async (e) =>
				{
					if (set == false)
					{
						Game game = new Game("One Hour Game Yam");
						discord.SetGame(game);

						await e.Channel.SendMessage("All Set!");

						set = true;
					}

				});
		}

		#endregion

		#region One Hour Game Jam Commands
		
		private void OHGJ_CreateTimeCommand(string command) 
		{
			commands.CreateCommand(command).Do(async e =>
			{
				await e.Channel.SendMessage("Time!");
			});
		}

		private void OHGJ_CreateThemeCommand(string command) //DONE!
		{

			commands.CreateCommand(command).Do(async e =>
			{
				await e.Channel.SendMessage("Theme!");
			});
		}

		#endregion

		private string GetJamInfo()
		{
			string jams;

			jams = client.DownloadString("http://onehourgamejam.com/api/nextjam");
			int i = jams.IndexOf("}],\"current_jams\"");



			 Console.WriteLine(i);

			return "";
		}
	}
}



