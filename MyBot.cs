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
		private DiscordClient discord;
		private CommandService commands;

		private Random random;

		private WebClient client = new WebClient();



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



			#region Commands
			random = new Random();
			commands = discord.GetService<CommandService>();


			SetCommand_INIT("set");

			OHGJ_CreateTimeCommand("time");
			OHGJ_CreateThemeCommand("theme");

			CreateTextCommand("vote", "Vote on the next theme here: http://onehourgamejam.com/?page=themes");

			CreateTextCommand("submit", "Submit your game here: http://onehourgamejam.com/?page=submit, **if you don't have an account yet type __!login__**");

			CreateTextCommand("login", "If you don't have an account yet or if you aren't logged in go here: http://onehourgamejam.com/?page=login");



			#endregion



			#region More Importand Stuff
			discord.ExecuteAndWait(async () => {
				await discord.Connect("", TokenType.Bot); //Insert token here
			});
			#endregion


			INIT();
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

		private void SetCommand_INIT(string command)
		{
			commands.CreateCommand(command).Do(
				async (e) =>
				{

					INIT();

					await e.Channel.SendMessage("All Set!");


				});
		}

		#endregion

		#region One Hour Game Jam Commands
		
		private void OHGJ_CreateTimeCommand(string command) 
		{
			commands.CreateCommand(command).Do(async e =>
			{
				string response = GetJamInfo(4);

				await e.Channel.SendMessage(response);
			});
		}

		private void OHGJ_CreateThemeCommand(string command)
		{

			commands.CreateCommand(command).Do(async e =>
			{
				string response = "The theme " + GetJamInfo(1);

				await e.Channel.SendMessage(response);
			});
		}

		#endregion

		#region One Hour Game Jam

		private string GetJamInfo(int infoIndex)
		{
			string jams;

			jams = client.DownloadString("http://onehourgamejam.com/api/nextjam");

			string[] info = jams.Split(new string[] { "]," }, StringSplitOptions.None);
			string now = GetNow(info[0]);

			string upcoming = info[0];
			upcoming = upcoming.Remove(0, 29);
			//Console.WriteLine(upcoming);

			Dictionary<int, string> Info = new Dictionary<int, string>();
			Info.Add(0, upcoming); // 0 -- Upcoming jams
			Info.Add(1, info[1]); // 1 -- Current jams
			Info.Add(2, info[2]); // 2 -- Previous jams
			Info.Add(3, now);     // 3 -- Now

			//foreach (var item in Info)
			//{
			//	Console.WriteLine(item);
			//}

			//------jamIndex----
			// 0 -- Upcoming jams
			// 1 -- Current jams
			// 2 -- Previous jams

			//-----infoIndex-----
			// 1 -- Theme
			// 4 -- Time difference

			string response = "";

			#region Debug
			//string test = "\"current_jams\":[{\"number\":106,\"theme\":\"Gold\",\"start_datetime\":\"2017-05-06 20:00:00\",\"timediff\":-1800}";

			//if (infoIndex == 1)
			//{
			//	if (IsJamOn(test))
			//	{
			//		response = "is: " + GetCurrentJams(test, 1);
			//	}
			//	else
			//	{
			//		response = "hasn't been announced yet.";
			//	}

			//}

			//if (infoIndex == 4)
			//{
			//	if (IsJamOn(test))
			//	{
			//		//Console.WriteLine(Info[0]);
			//		response = GetTime(GetCurrentJams(test, 3), true) + " left.";
			//	}
			//	else
			//	{
			//		response = GetTime(GetUpcomingJam(test, 3), false) + " until the jam.";
			//	}
			//}

			#endregion


			#region Theme
			if (infoIndex == 1)
			{
				if (IsJamOn(Info[1]))
				{
					response = "is: " + GetCurrentJams(Info[1], 1);
				}
				else
				{
					response = "hasn't been announced yet.";
				}

			}
			#endregion

			#region Time
			else if (infoIndex == 4)
			{
				if (IsJamOn(Info[1])) // The jam is on!
				{
					response = GetTime(GetCurrentJams(Info[1], 3), true) + " left.";
				}
				else
				{
					//Console.WriteLine("Jam not on");
					response = GetTime(GetUpcomingJam(Info[0], 3), false) + " left until the next jam.";
				}
			}
			#endregion



			return response;
		}
		

		private string GetUpcomingJam(string jams, int index)
		{
			jams = jams.Remove(0, 19);
			jams = jams.Replace("}", "");

			string[] info = jams.Split(',');

			Dictionary<int, string> Info = new Dictionary<int, string>();

			int i = 0;
			foreach (var item in info)
			{
				//Console.WriteLine(item);
				string[] s = item.Split(new string[] { "\":" }, StringSplitOptions.None);
				string S = s[1]; //.Remove(s[1].Length - 1);
				//Console.WriteLine(S);

				Info.Add(i, S);
				i++;
			}

			//foreach (var item in Info)
			//{
			//	Console.WriteLine(item);
			//}


			// 0 -- Jam number
			// 1 -- Theme
			// 2 -- Start Time
			// 3 -- Time difference

			return Info[index];
		}

		private string GetCurrentJams(string jam, int index)
		{
			string jams = jam.Remove(0, 17);

			jams = jams.Replace("}", "");

			string[] info = jams.Split(',');

			Dictionary<int, string> Info = new Dictionary<int, string>();

			int i = 0;
			foreach (var item in info)
			{
				string[] s = item.Split(new string[] { "\":" }, StringSplitOptions.None);
				string S = s[1];//.Remove(s[1].Length - 1);


				Info.Add(i, S);
				i++;
			}

			//foreach (var item in Info)
			//{
			//	Console.WriteLine(item);
			//}

			// 0 -- Jam number
			// 1 -- Theme
			// 2 -- Start Time
			// 3 -- Time difference

			return Info[index];
		}

		private string GetNow(string str)
		{
			string[] time = str.Split(new string[] { "," }, StringSplitOptions.None);

			string now = time[0].Replace("{\"now\":\"", String.Empty);
			now = now.Replace("\"", String.Empty);

			return now;
		}

		private bool IsJamOn(string jam)
		{
			string test = jam.Remove(0, 16);
			if (test == "")
			{
				//Console.WriteLine("No current jam");
				return false;
			}
			else
				return true;

		}

		private string GetTime(string timeDiff, bool jamOn)
		{
			int i = Int32.Parse(timeDiff) + 7200;
			string response = "";
			

			if (jamOn == false)
			{

				i = Math.Abs(i);

				if (i / 60 < 1) // SEC
					response = i.ToString() + " second" + Plurality(i);

				if (i / 60 >= 1) // MIN
				{
					response = (i / 60).ToString() + " minute" + Plurality(i / 60);
					int sec = (i % 60);
					response += " " + sec + " second" + Plurality(sec);
				}

				if (i / 3600 >= 1) // HOUR
				{
					response = (i / 3600).ToString() + " hour" + Plurality(i / 3600);
					int min = (i % 3600) / 60;
					response += " " + min + " minute" + Plurality(min);
				}

				if (i / 86400 >= 1) // DAY
				{
					response = (i / 86400).ToString() + " day" + Plurality(i / 86400);

					int hour = (i % 86400) / 3600;
					response += " " + hour + " hour" + Plurality(hour);

					int min = ((i % 86400) % 3600) / 60;
					response += " " + min + " minute" + Plurality(min);
				}


			}
			else
			{

				if (i / 60 < 1) // SEC
					response = i.ToString() + " second" + Plurality(i);

				if ((3600 + i) / 60 >= 1) // MIN
				{
					response = ((3600 + i) / 60).ToString() + " minute" + Plurality((3600 + i) / 60);

					int sec = ((3600 + i) % 60);
					response += " " + sec + " second" + Plurality(sec);
				}
			}

			return response;
		}

		private string Plurality(int i)
		{
			string response = "";
			if (i == 1)
			{
				response = "";
			}
			else
			{
				response = "s";
			}

			return response;
		}

		#endregion


		private void INIT()
		{
			Game game = new Game("One Hour Game Yam");
			discord.SetGame(game);
		}
	}
}



