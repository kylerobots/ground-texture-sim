#include "DataSynchronizer.h"

#include "gtest/gtest.h"

/**
 * @brief Tests that the synchronizer works when requesting no topics.
 * 
 */
TEST(DataSynchronizer, Empty) {
	ground_texture_sim::DataSynchronizer synchronizer;
	auto results = synchronizer.getMessages();
	EXPECT_EQ(results.size(), 0);
}