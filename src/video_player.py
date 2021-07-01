"""A video player class."""

from .video_library import VideoLibrary
import random
import sys

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.playing = None
        self.paused = False
        self.playlists_names = []
        self.playlists = {}
        self.flagged_videos = {}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        video_items_list = self._video_library.get_all_videos()
        all_videos_list = []
        for video_items in video_items_list:
            all_videos_list.append(video_items.title + " (" + video_items.video_id + ") [" + ' '.join(video_items.tags) + "]")

        all_videos_list.sort()
        for item in all_videos_list:
            print("    " + item)

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        if self._video_library.get_video(video_id) in self._video_library.get_all_videos():
            if self._video_library.get_video(video_id) in self.flagged_videos:
                print("Cannot play video: Video is currently flagged (reason: " + self.flagged_videos[self._video_library.get_video(video_id)] + ")")
            else:
                self.paused = False
                if self.playing:
                    print("Stopping video: " + self.playing.title)
                print("Playing video: " + self._video_library.get_video(video_id).title)
                self.playing = self._video_library.get_video(video_id)
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self.playing:
            print("Stopping video: " + self.playing.title)
            self.playing = None
        else:
            print("Cannot stop video: No video is currently playing")

    def play_random_video(self):
        """Plays a random video from the video library."""
        available_videos = list(set(self._video_library.get_all_videos()).difference(self.flagged_videos.keys()))
        if len(available_videos) > 0:
            self.play_video(random.choice(available_videos).video_id)
        else:
            print("No videos available")
        #print("play_random_video needs implementation")

    def pause_video(self):
        """Pauses the current video."""

        if self.playing:
            if self.paused:
                print("Video already paused: " + self.playing.title)
            else:
                print("Pausing video: " + self.playing.title)
                self.paused = True
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.playing:
            if self.paused:
                print("Continuing video: " + self.playing.title)
                self.paused = False
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        if self.playing:
            print("Currently playing: " + self.playing.title + " (" + self.playing.video_id + ") [" + ' '.join(self.playing.tags) + "]" + (" - PAUSED" if self.paused else ""))
        else:
            print("No video is currently playing")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        if playlist_name.lower() in self.playlists:
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlists_names.append(playlist_name)
            self.playlists[playlist_name.lower()] = []
            print("Successfully created new playlist: " + playlist_name)




    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.lower() in self.playlists.keys():
            if self._video_library.get_video(video_id) not in self._video_library.get_all_videos():
                print("Cannot add video to " + playlist_name + ": Video does not exist")
            elif video_id in self.playlists[playlist_name.lower()]:
                print("Cannot add video to " + playlist_name + ": Video already added")
            else:
                self.playlists[playlist_name.lower()] += [video_id]
                print("Added video to " + playlist_name + ": " + self._video_library.get_video(video_id).title)
        else:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")



    def show_all_playlists(self):
        """Display all playlists."""
        if len(self.playlists_names) == 0:
            print("No playlists exist yet")
        else:
            print("Showing all playlists:")
            playlist_names = self.playlists_names
            playlist_names.sort()
            for playlist_name in playlist_names:
                print(playlist_name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.playlists.keys():
            print("Showing playlist: " + playlist_name)
            if(len(self.playlists[playlist_name.lower()]) == 0):
                print("No videos here yet")
            else:

                for item in self.playlists[playlist_name.lower()]:

                    print(self._video_library.get_video(item).title + " (" + self._video_library.get_video(item).video_id + ") [" + ' '.join(self._video_library.get_video(item).tags) + "]")
        else:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.lower() in self.playlists.keys():
            if video_id in self.playlists[playlist_name.lower()]:
                self.playlists[playlist_name.lower()].remove(video_id)
                print("Removed video from " + playlist_name + ": " + self._video_library.get_video(video_id).title)


            elif self._video_library.get_video(video_id) in self._video_library.get_all_videos():
                print("Cannot remove video from " + playlist_name + ": Video is not in playlist")
            else:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")
        else:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.playlists.keys():
            self.playlists[playlist_name.lower()] = []
            print("Successfully removed all videos from " + playlist_name)

        else:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist" )

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.lower() in self.playlists.keys():
            print("Deleted playlist: " + playlist_name + "")
            self.playlists.pop(playlist_name.lower(), None)
            self.playlists_names.remove(playlist_name)
        else:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        video_items_list = self._video_library.get_all_videos()
        all_videos_list = []
        for video_items in video_items_list:
            #print(video_items.title)
            if(search_term in video_items.title.lower()):
                all_videos_list.append(video_items.title + " (" + video_items.video_id + ") [" + ' '.join(video_items.tags) + "]")


        if(len(all_videos_list) > 0):
            all_videos_list.sort()
            print("Here are the results for " + search_term + ":")
            for i,item in enumerate(all_videos_list):
                print(str(i+1) + ") " + item)
            print("Would you like to play any of the above? If yes, "
                  "specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            inp = input()
            if inp != "No":
                try:
                    if int(inp[0]) in range(1,len(all_videos_list)+1):

                        self.play_video(all_videos_list[int(inp[0])-1][all_videos_list[int(inp[0])-1].find("(")+1:all_videos_list[int(inp[0])-1].find(")")])
                except:
                    pass
        else:
            print("No search results for " + search_term)
        #for video_id in self._video_library.get_all_videos():

        #print("search_videos needs implementation")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        video_items_list = self._video_library.get_all_videos()
        all_videos_list = []
        for video_items in video_items_list:
            #print(video_items.title)
            if(video_tag.lower() in video_items.tags):
                all_videos_list.append(video_items.title + " (" + video_items.video_id + ") [" + ' '.join(video_items.tags) + "]")


        if(len(all_videos_list) > 0):
            all_videos_list.sort()
            print("Here are the results for " + video_tag + ":")
            for i,item in enumerate(all_videos_list):
                print(str(i+1) + ") " + item)
            print("Would you like to play any of the above? If yes, "
                  "specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")

            inp = input()
            if inp != "No":
                try:
                    if int(inp[0]) in range(1,len(all_videos_list)+1):

                        self.play_video(all_videos_list[int(inp[0])-1][all_videos_list[int(inp[0])-1].find("(")+1:all_videos_list[int(inp[0])-1].find(")")])
                except:
                    pass
        else:
            print("No search results for " + video_tag)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if self._video_library.get_video(video_id) in self._video_library.get_all_videos():
            if(self._video_library.get_video(video_id) not in self.flagged_videos.keys()):
                print("Successfully flagged video: "+ self._video_library.get_video(video_id).title + " (reason: "+(flag_reason if flag_reason!="" else "Not supplied")+")")
                self.flagged_videos[self._video_library.get_video(video_id)] = (flag_reason if flag_reason!="" else "Not supplied")
            else:
                print("Cannot flag video: Video is already flagged")
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
