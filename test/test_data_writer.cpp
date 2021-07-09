#include "DataWriter.h"

#include "gtest/gtest.h"
#include <filesystem>

/// @test Make sure the system can work when given no specific path.
TEST(DataWriter, Empty) {
	ASSERT_NO_THROW(ground_texture_sim::DataWriter());
}