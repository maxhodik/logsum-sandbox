package com.sandbox;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

public class LogSum {

    private static class GroupStats {
        int count = 0;
        String firstSeen = null;
        String lastSeen = null;
    }

    private record GroupKey(String service, String level) {}

    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: java com.sandbox.LogSum <input_csv> <output_csv>");
            System.exit(1);
        }

        Path inputPath = Paths.get(args[0]);
        Path outputPath = Paths.get(args[1]);

        Map<GroupKey, GroupStats> groups = new HashMap<>();

        try (BufferedReader reader = Files.newBufferedReader(inputPath)) {
            String headerLine = reader.readLine();
            if (headerLine == null) {
                System.err.println("Error: Empty input file.");
                System.exit(1);
            }

            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",", -1);
                if (parts.length < 4) continue;

                String timestamp = parts[0].trim();
                String level = parts[1].trim();
                if (level.isEmpty()) {
                    level = "UNKNOWN";
                }
                String service = parts[2].trim();

                GroupKey key = new GroupKey(service, level);
                GroupStats stats = groups.computeIfAbsent(key, k -> new GroupStats());

                stats.count++;
                if (stats.firstSeen == null || timestamp.compareTo(stats.firstSeen) < 0) {
                    stats.firstSeen = timestamp;
                }
                if (stats.lastSeen == null || timestamp.compareTo(stats.lastSeen) > 0) {
                    stats.lastSeen = timestamp;
                }
            }

        } catch (IOException e) {
            System.err.println("Error reading input file: " + e.getMessage());
            System.exit(1);
        }

        try (BufferedWriter writer = Files.newBufferedWriter(outputPath)) {
            writer.write("service,level,count,first_seen,last_seen\n");
            for (Map.Entry<GroupKey, GroupStats> entry : groups.entrySet()) {
                GroupKey key = entry.getKey();
                GroupStats stats = entry.getValue();
                writer.write(String.format("%s,%s,%d,%s,%s\n",
                        key.service(), key.level(), stats.count, stats.firstSeen, stats.lastSeen));
            }
            System.out.println("Summary successfully written to " + outputPath);
        } catch (IOException e) {
            System.err.println("Error writing output file: " + e.getMessage());
            System.exit(1);
        }
    }
}