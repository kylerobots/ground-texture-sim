#include "DataSynchronizer.h"

namespace ground_texture_sim {
	DataSynchronizer::DataSynchronizer() {
	}

	std::map<std::string, std::shared_ptr<google::protobuf::Message>> DataSynchronizer::getMessages() {
		// When called, alert all the topics to actually write new messages.
		for (auto it = capture_flags.begin(); it != capture_flags.end(); ++it) {
			it->second = true;
		}
		// Now just wait until all messages have been updated.
		bool all_captured = true;
		while (!all_captured) {
			for (auto & capture_flag : capture_flags) {
				all_captured &= capture_flag.second;
			}
		}
		// Once done, return the map, which will copy it out.
		return synched_messages;
	}
} // namespace ground_texture_sim
