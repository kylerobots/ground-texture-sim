#include "DataSynchronizer.h"

namespace ground_texture_sim {
	DataSynchronizer::DataSynchronizer() {
	}

	std::map<std::string, std::unique_ptr<google::protobuf::Message>> DataSynchronizer::getMessages() {
		std::map<std::string, std::unique_ptr<google::protobuf::Message>> messages;
		return messages;
	}

	template <typename T>
	void DataSynchronizer::messageCallback(const T & message, const ignition::transport::MessageInfo & info) {
		std::string topic_name = info.Topic();
		// Only record if requested to.
		if (capture_flags.at(topic_name)) {
			synched_messages[topic_name].reset(std::make_unique<T>(message));
			capture_flags[topic_name] = false;
		}
	}

	template <typename T>
	bool DataSynchronizer::registerTopic(const std::string & topic_name) {
		bool success = node.Subscribe(topic_name, &DataSynchronizer::messageCallback<T>, this);
		if (success) {
			capture_flags[topic_name] = false;
		}
		return success;
	}
} // namespace ground_texture_sim
