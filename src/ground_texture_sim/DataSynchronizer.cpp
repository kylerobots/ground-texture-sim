#include "DataSynchronizer.h"

namespace ground_texture_sim {
	DataSynchronizer::DataSynchronizer() {
	}

	std::map<std::string, std::unique_ptr<google::protobuf::Message>> DataSynchronizer::getMessages() {
		std::map<std::string, std::unique_ptr<google::protobuf::Message>> messages;
		return messages;
	}
} // namespace ground_texture_sim
