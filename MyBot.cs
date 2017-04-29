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



			#region Commands
			random = new Random();
			commands = discord.GetService<CommandService>();

			INIT("set");

			OHGJ_CreateTimeCommand("time");
			OHGJ_CreateThemeCommand("theme");
			#endregion



			#region More Importand Stuff
			discord.ExecuteAndWait(async () => {
				await discord.Connect("", TokenType.Bot);
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
				string response = GetJamInfo(4);

				await e.Channel.SendMessage(response);
			});
		}

		private void OHGJ_CreateThemeCommand(string command) //DONE!
		{

			commands.CreateCommand(command).Do(async e =>
			{
				string response = "The theme " + GetJamInfo(1);

				await e.Channel.SendMessage(response);
			});
		}

		#endregion

		private string GetJamInfo(int infoIndex)
		{
			string jams;

			jams = client.DownloadString("http://onehourgamejam.com/api/nextjam");

			string[] info = jams.Split(new string[] { "]," }, StringSplitOptions.None);

			Dictionary<int, string> Info = new Dictionary<int, string>();
			Info.Add(0, info[0]); // 0 -- Upcoming jams
			Info.Add(1, info[1]); // 1 -- Current jams
			Info.Add(2, info[2]); // 2 -- Previous jams

			//foreach (var item in Info)
			//{
			//	Console.WriteLine(item);
			//}

			//------jamIndex----
			// 0 -- Upcoming jams
			// 1 -- Current jams
			// 2 -- Previous jams

			//-----infoIndex-----
			// 0 -- Jam number
			// 1 -- Theme
			// 2 -- Start Time
			// 3 -- Current Time
			// 4 -- Time difference

			string response = "";


			#region Debug
			//string test = "\"current_jams\":[{\"number\":\"105\",\"theme\":\"Random Theme by Devil\",\"start_datetime\":\"2017-04-29 20:00:00\",\"now\":\"2017-04-29 20:30:00\",\"timediff\":\"-272586\"}";

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
			//	if (IsJamOn(Info[1]))
			//	{
			//		response = GetTime(GetCurrentJams(test, 4), true) + " left.";
			//	}
			//	else
			//	{
			//		response = GetTime(GetCurrentJams(test, 4), false) + " until the jam.";
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
				if (IsJamOn(Info[1]))
				{
					response = GetTime(GetCurrentJams(Info[1], 4), true) + " left.";
				}
				else
				{
					response = GetTime(GetCurrentJams(Info[0], 4), false) + " left until the next jam.";
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
				string[] s = item.Split(new string[] { "\":\"" }, StringSplitOptions.None);
				string S = s[1].Remove(s[1].Length - 1);


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
			// 3 -- Current Time
			// 4 -- Time difference

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
					string[] s = item.Split(new string[] { "\":\"" }, StringSplitOptions.None);
					string S = s[1].Remove(s[1].Length - 1);


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
			// 3 -- Current Time
			// 4 -- Time difference

			return Info[index];
		}

		private bool IsJamOn(string jam)
		{
			//Console.WriteLine(jam);
			string test = jam.Remove(0, 16);

			if (test == "")
			{
				//Console.WriteLine("No current jam");
				return false;
			}
			else
				return true;

		}

		private string GetTime(string time, bool jamOn)
		{
			int i = Int32.Parse(time);
			string response = "";
			

			if (jamOn == false)
			{
				
				i = Math.Abs(i);

				if (i / 60 < 1) // SEC
					response = i.ToString() + " second" + theSthing(i);

				if (i / 60 >= 1) // MIN
				{
					response = (i / 60).ToString() + " minute" + theSthing(i / 60);
					int sec = (i % 60);					
					response += " " + sec + " second" + theSthing(sec);
				}
					
				if (i / 3600 >= 1) // HOUR
				{
					response= (i / 3600).ToString() + " hour" + theSthing(i / 3600);
					int min = (i % 3600) / 60;
					response += " " + min + " minute" + theSthing(min);
				}

				if (i / 86400 >= 1) // DAY
				{
					response = (i / 86400).ToString() + " day" + theSthing(i / 86400);

					int hour = (i % 86400) / 3600;
					response += " " + hour + " hour" + theSthing(hour);

					int min = ((i % 86400) % 3600) / 60;
					response += " " + min + " minute" + theSthing(min);
				}

			}
			else
			{

				if (i / 60 < 1) // SEC
					response = i.ToString() + " second" + theSthing(i);

				if ((3600 + i) / 60 >= 1) // MIN
				{
					response = ((3600 + i) / 60).ToString() + " minute" + theSthing((3600 + i) / 60);

					int sec = ((3600 + i) % 60);
					response += " " + sec + " second" + theSthing(sec);
				}
			}

			return response;
		}


		private string theSthing(int i)
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
	}
}