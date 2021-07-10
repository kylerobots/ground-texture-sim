#include "DataSynchronizer.h"

#include "gtest/gtest.h"

/// @test Tests that the synchronizer works when requesting no topics.
TEST(DataSynchronizer, Empty) {
	ground_texture_sim::DataSynchronizer synchronizer;
	auto results = synchronizer.getMessages();
	EXPECT_EQ(results.size(), 0);
}

/// @test Tests that the synchronizer can subscribe to multiple topics of different types.
TEST(DataSynchronizer, Subscribe) {
	ground_texture_sim::DataSynchronizer synchronizer;
	bool success = true;
	success &= synchronizer.registerTopic<ignition::msgs::Image>("/camera");
	success &= synchronizer.registerTopic<ignition::msgs::Pose>("/pose");
	EXPECT_TRUE(success);
}