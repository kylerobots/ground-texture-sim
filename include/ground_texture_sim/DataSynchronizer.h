#ifndef _DATA_SYNCHRONIZER_H_
#define _DATA_SYNCHRONIZER_H_

#include <ignition/msgs.hh>
#include <ignition/transport.hh>
#include <map>
#include <memory>
#include <string>

/**
 * @brief The namespace for any class created in this package.
 * 
 * This is mainly implemented to prevent possible collisions with similarly named entities.
 * 
 */
namespace ground_texture_sim {
	/**
	 * @brief A class to automatically subscribe to multiple topics and coordinate their returned values.
	 * 
	 * This class subscribes to multiple Ignition message topics. It synchronizes them by retreiving the next message
	 * after a request for data has been made. Future iterations could add additional techniques, such as nearest
	 * message or interpolation.
	 * 
	 * An arbitrary number of messages are supported.
	 * 
	 */
	class DataSynchronizer {
		public:
		/**
		 * @brief Construct a new Data Synchronizer object
		 * 
		 */
		DataSynchronizer();

		/**
		 * @brief Get synchronized messages received after the call.
		 * 
		 * This function blocks until one message from each registered topic is received. Once they are all received,
		 * the messages are returned in a map. The topic name is the key for each message.
		 * 
		 * @return std::map<std::string, std::unique_ptr<google::protobuf::Message>> The map containing the messages.
		 * Because the parent class is abstract, the values are pointers to the messages. This assumes that you know
		 * or can figure out what specific message type each is.
		 */
		std::map<std::string, std::unique_ptr<google::protobuf::Message>> getMessages();

		/**
		 * @brief Register a given topic name to synchronize its data with the other topics.
		 * 
		 * This will instruct the object that the provided topic is one that should be synchronized when getMessages is
		 * called. If the registration fails, a false value will be returned and the topic will not be part of the list
		 * of topics. This may happen if the system is unable to subscribe to the topic.
		 * 
		 * @param topic_name The topic name to attempt to register.
		 * @return true If the topic was registered successfully.
		 * @return false If the topic was not registered.
		 */
		template <typename T>
		bool registerTopic(const std::string & topic_name);

		protected:
		template <typename T>
		void messageCallback(const T & message, const ignition::transport::MessageInfo & info);

		protected:
		/// Flags to indicate that a message should be recorded.
		std::map<std::string, bool> capture_flags;
		/// The messages recorded when the capture_flag is set to true.
		std::map<std::string, std::unique_ptr<google::protobuf::Message>> synched_messages;
		/// The node used to subscribe to topics.
		ignition::transport::Node node;
	};

} // namespace ground_texture_sim

#endif // _DATA_SYNCHRONIZER_H_