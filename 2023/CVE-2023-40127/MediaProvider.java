/*
 * Copyright (C) 2006 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.android.providers.media;

import static android.app.PendingIntent.FLAG_CANCEL_CURRENT;
import static android.app.PendingIntent.FLAG_IMMUTABLE;
import static android.app.PendingIntent.FLAG_ONE_SHOT;
import static android.content.pm.PackageManager.PERMISSION_GRANTED;
import static android.os.Environment.buildPath;
import static android.os.Trace.TRACE_TAG_DATABASE;
import static android.provider.MediaStore.AUTHORITY;
import static android.provider.MediaStore.Downloads.PATTERN_DOWNLOADS_FILE;
import static android.provider.MediaStore.Downloads.isDownload;
import static android.provider.MediaStore.getVolumeName;

import static com.android.providers.media.LocalCallingIdentity.PERMISSION_IS_LEGACY;
import static com.android.providers.media.LocalCallingIdentity.PERMISSION_IS_REDACTION_NEEDED;
import static com.android.providers.media.LocalCallingIdentity.PERMISSION_IS_SYSTEM;
import static com.android.providers.media.LocalCallingIdentity.PERMISSION_READ_AUDIO;
import static com.android.providers.media.LocalCallingIdentity.PERMISSION_READ_IMAGES;
import static com.android.providers.media.LocalCallingIdentity.PERMISSION_READ_VIDEO;
import static com.android.providers.media.LocalCallingIdentity.PERMISSION_WRITE_AUDIO;
import static com.android.providers.media.LocalCallingIdentity.PERMISSION_WRITE_IMAGES;
import static com.android.providers.media.LocalCallingIdentity.PERMISSION_WRITE_VIDEO;

import android.annotation.BytesLong;
import android.annotation.NonNull;
import android.annotation.Nullable;
import android.app.AppGlobals;
import android.app.AppOpsManager;
import android.app.AppOpsManager.OnOpActiveChangedListener;
import android.app.PendingIntent;
import android.app.RecoverableSecurityException;
import android.app.RemoteAction;
import android.content.BroadcastReceiver;
import android.content.ContentProvider;
import android.content.ContentProviderClient;
import android.content.ContentProviderOperation;
import android.content.ContentProviderResult;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.OperationApplicationException;
import android.content.SharedPreferences;
import android.content.UriMatcher;
import android.content.pm.PackageManager;
import android.content.pm.PackageManager.NameNotFoundException;
import android.content.pm.PermissionGroupInfo;
import android.content.res.AssetFileDescriptor;
import android.content.res.Configuration;
import android.content.res.Resources;
import android.database.AbstractCursor;
import android.database.Cursor;
import android.database.DatabaseUtils;
import android.database.MatrixCursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.database.sqlite.SQLiteQueryBuilder;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.Icon;
import android.media.ExifInterface;
import android.media.MediaFile;
import android.media.ThumbnailUtils;
import android.mtp.MtpConstants;
import android.net.Uri;
import android.os.Binder;
import android.os.Build;
import android.os.Bundle;
import android.os.CancellationSignal;
import android.os.Environment;
import android.os.FileUtils;
import android.os.IBinder;
import android.os.ParcelFileDescriptor;
import android.os.ParcelFileDescriptor.OnCloseListener;
import android.os.RedactingFileDescriptor;
import android.os.RemoteException;
import android.os.SystemClock;
import android.os.SystemProperties;
import android.os.Trace;
import android.os.UserHandle;
import android.os.UserManager;
import android.os.storage.StorageEventListener;
import android.os.storage.StorageManager;
import android.os.storage.StorageVolume;
import android.os.storage.VolumeInfo;
import android.os.storage.VolumeRecord;
import android.preference.PreferenceManager;
import android.provider.BaseColumns;
import android.provider.Column;
import android.provider.DocumentsContract;
import android.provider.MediaStore;
import android.provider.MediaStore.Audio;
import android.provider.MediaStore.Audio.AudioColumns;
import android.provider.MediaStore.Audio.Playlists;
import android.provider.MediaStore.Downloads;
import android.provider.MediaStore.Files;
import android.provider.MediaStore.Files.FileColumns;
import android.provider.MediaStore.Images;
import android.provider.MediaStore.Images.ImageColumns;
import android.provider.MediaStore.MediaColumns;
import android.provider.MediaStore.Video;
import android.system.ErrnoException;
import android.system.Os;
import android.system.OsConstants;
import android.system.StructStat;
import android.text.TextUtils;
import android.text.format.DateUtils;
import android.util.ArrayMap;
import android.util.ArraySet;
import android.util.DisplayMetrics;
import android.util.Log;
import android.util.LongArray;
import android.util.LongSparseArray;
import android.util.Pair;
import android.util.Size;
import android.util.SparseArray;

import com.android.internal.annotations.GuardedBy;
import com.android.internal.annotations.VisibleForTesting;
import com.android.internal.os.BackgroundThread;
import com.android.internal.util.ArrayUtils;
import com.android.internal.util.IndentingPrintWriter;
import com.android.providers.media.scan.MediaScanner;
import com.android.providers.media.scan.ModernMediaScanner;
import com.android.providers.media.util.CachedSupplier;
import com.android.providers.media.util.IsoInterface;
import com.android.providers.media.util.XmpInterface;

import libcore.io.IoUtils;
import libcore.util.EmptyArray;

import java.io.File;
import java.io.FileDescriptor;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FilenameFilter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.TimeUnit;
import java.util.function.Consumer;
import java.util.function.Supplier;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Media content provider. See {@link android.provider.MediaStore} for details.
 * Separate databases are kept for each external storage card we see (using the
 * card's ID as an index).  The content visible at content://media/external/...
 * changes with the card.
 */
public class MediaProvider extends ContentProvider {
    public static final boolean ENABLE_MODERN_SCANNER = SystemProperties
            .getBoolean("persist.sys.modern_scanner", true);

    /**
     * Regex that matches paths in all well-known package-specific directories,
     * and which captures the package name as the first group.
     */
    private static final Pattern PATTERN_OWNED_PATH = Pattern.compile(
            "(?i)^/storage/[^/]+/(?:[0-9]+/)?Android/(?:data|media|obb|sandbox)/([^/]+)/.*");

    /**
     * Regex that matches paths under well-known storage paths.
     */
    private static final Pattern PATTERN_STORAGE_PATH = Pattern.compile(
            "(?i)^/storage/[^/]+/(?:[0-9]+/)?");

    /**
     * Regex that matches paths for {@link MediaColumns#RELATIVE_PATH}; it
     * captures both top-level paths and sandboxed paths.
     */
    private static final Pattern PATTERN_RELATIVE_PATH = Pattern.compile(
            "(?i)^/storage/[^/]+/(?:[0-9]+/)?(Android/sandbox/([^/]+)/)?");

    /**
     * Regex that matches paths under well-known storage paths.
     */
    private static final Pattern PATTERN_VOLUME_NAME = Pattern.compile(
            "(?i)^/storage/([^/]+)");

    /**
     * Regex of a selection string that matches a specific ID.
     */
    private static final Pattern PATTERN_SELECTION_ID = Pattern.compile(
            "(?:image_id|video_id)\\s*=\\s*(\\d+)");

    /**
     * Set of {@link Cursor} columns that refer to raw filesystem paths.
     */
    private static final ArrayMap<String, Object> sDataColumns = new ArrayMap<>();

    {
        sDataColumns.put(MediaStore.MediaColumns.DATA, null);
        sDataColumns.put(MediaStore.Images.Thumbnails.DATA, null);
        sDataColumns.put(MediaStore.Video.Thumbnails.DATA, null);
        sDataColumns.put(MediaStore.Audio.PlaylistsColumns.DATA, null);
        sDataColumns.put(MediaStore.Audio.AlbumColumns.ALBUM_ART, null);
    }

    private static final Object sCacheLock = new Object();

    @GuardedBy("sCacheLock")
    private static final List<VolumeInfo> sCachedVolumes = new ArrayList<>();
    @GuardedBy("sCacheLock")
    private static final Set<String> sCachedExternalVolumeNames = new ArraySet<>();
    @GuardedBy("sCacheLock")
    private static final Map<String, Collection<File>> sCachedVolumeScanPaths = new ArrayMap<>();

    private void updateVolumes() {
        synchronized (sCacheLock) {
            sCachedVolumes.clear();
            sCachedVolumes.addAll(mStorageManager.getVolumes());

            sCachedExternalVolumeNames.clear();
            sCachedExternalVolumeNames.addAll(MediaStore.getExternalVolumeNames(getContext()));

            sCachedVolumeScanPaths.clear();
            try {
                sCachedVolumeScanPaths.put(MediaStore.VOLUME_INTERNAL,
                        MediaStore.getVolumeScanPaths(MediaStore.VOLUME_INTERNAL));
                for (String volumeName : sCachedExternalVolumeNames) {
                    sCachedVolumeScanPaths.put(volumeName,
                            MediaStore.getVolumeScanPaths(volumeName));
                }
            } catch (FileNotFoundException e) {
                throw new IllegalStateException(e.getMessage());
            }
        }
    }

    public static File getVolumePath(String volumeName) throws FileNotFoundException {
        synchronized (sCacheLock) {
            return MediaStore.getVolumePath(sCachedVolumes, volumeName);
        }
    }

    public static Set<String> getExternalVolumeNames() {
        synchronized (sCacheLock) {
            return new ArraySet<>(sCachedExternalVolumeNames);
        }
    }

    public static Collection<File> getVolumeScanPaths(String volumeName) {
        synchronized (sCacheLock) {
            return new ArrayList<>(sCachedVolumeScanPaths.get(volumeName));
        }
    }

    private StorageManager mStorageManager;
    private AppOpsManager mAppOpsManager;
    private PackageManager mPackageManager;

    private Size mThumbSize;

    /**
     * Map from UID to cached {@link LocalCallingIdentity}. Values are only
     * maintained in this map while the UID is actively working with a
     * performance-critical component, such as camera.
     */
    @GuardedBy("mCachedCallingIdentity")
    private final SparseArray<LocalCallingIdentity> mCachedCallingIdentity = new SparseArray<>();

    private static volatile long sBackgroundDelay = 0;

    private final OnOpActiveChangedListener mActiveListener = (code, uid, packageName, active) -> {
        synchronized (mCachedCallingIdentity) {
            if (active) {
                mCachedCallingIdentity.put(uid,
                        LocalCallingIdentity.fromExternal(uid, packageName));
            } else {
                mCachedCallingIdentity.remove(uid);
            }

            if (mCachedCallingIdentity.size() > 0) {
                sBackgroundDelay = 10 * DateUtils.SECOND_IN_MILLIS;
            } else {
                sBackgroundDelay = 0;
            }
        }
    };

    /**
     * Calling identity state about on the current thread. Populated on demand,
     * and invalidated by {@link #onCallingPackageChanged()} when each remote
     * call is finished.
     */
    private final ThreadLocal<LocalCallingIdentity> mCallingIdentity = ThreadLocal
            .withInitial(() -> {
                synchronized (mCachedCallingIdentity) {
                    final LocalCallingIdentity cached = mCachedCallingIdentity
                            .get(Binder.getCallingUid());
                    return (cached != null) ? cached : LocalCallingIdentity.fromBinder(this);
                }
            });

    // In memory cache of path<->id mappings, to speed up inserts during media scan
    @GuardedBy("mDirectoryCache")
    private final ArrayMap<String, Long> mDirectoryCache = new ArrayMap<>();

    private static final String[] sMediaTableColumns = new String[] {
            FileColumns._ID,
            FileColumns.MEDIA_TYPE,
    };

    private static final String[] sIdOnlyColumn = new String[] {
        FileColumns._ID
    };

    private static final String[] sDataOnlyColumn = new String[] {
        FileColumns.DATA
    };

    private static final String[] sPlaylistIdPlayOrder = new String[] {
        Playlists.Members.PLAYLIST_ID,
        Playlists.Members.PLAY_ORDER
    };

    private static final String ID_NOT_PARENT_CLAUSE =
            "_id NOT IN (SELECT parent FROM files)";

    private static final String CANONICAL = "canonical";

    private BroadcastReceiver mMediaReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            final StorageVolume sv = intent.getParcelableExtra(StorageVolume.EXTRA_STORAGE_VOLUME);
            if (sv != null) {
                final String volumeName;
                if (sv.isPrimary()) {
                    volumeName = MediaStore.VOLUME_EXTERNAL_PRIMARY;
                } else {
                    try {
                        volumeName = MediaStore.checkArgumentVolumeName(sv.getNormalizedUuid());
                    } catch (IllegalArgumentException ignored) {
                        return;
                    }
                }

                switch (intent.getAction()) {
                    case Intent.ACTION_MEDIA_MOUNTED:
                        attachVolume(volumeName);
                        break;
                    case Intent.ACTION_MEDIA_UNMOUNTED:
                    case Intent.ACTION_MEDIA_EJECT:
                    case Intent.ACTION_MEDIA_REMOVED:
                    case Intent.ACTION_MEDIA_BAD_REMOVAL:
                        detachVolume(volumeName);
                        break;
                }
            }
        }
    };

    private final SQLiteDatabase.CustomFunction mObjectRemovedCallback =
                new SQLiteDatabase.CustomFunction() {
        @Override
        public void callback(String[] args) {
            // We could remove only the deleted entry from the cache, but that
            // requires the path, which we don't have here, so instead we just
            // clear the entire cache.
            // TODO: include the path in the callback and only remove the affected
            // entry from the cache
            synchronized (mDirectoryCache) {
                mDirectoryCache.clear();
            }
        }
    };

    /**
     * Wrapper class for a specific database (associated with one particular
     * external card, or with internal storage).  Can open the actual database
     * on demand, create and upgrade the schema, etc.
     */
    static class DatabaseHelper extends SQLiteOpenHelper implements AutoCloseable {
        final Context mContext;
        final String mName;
        final int mVersion;
        final boolean mInternal;  // True if this is the internal database
        final boolean mEarlyUpgrade;
        final SQLiteDatabase.CustomFunction mObjectRemovedCallback;
        long mScanStartTime;
        long mScanStopTime;

        // In memory caches of artist and album data.
        ArrayMap<String, Long> mArtistCache = new ArrayMap<String, Long>();
        ArrayMap<String, Long> mAlbumCache = new ArrayMap<String, Long>();

        public DatabaseHelper(Context context, String name, boolean internal,
                boolean earlyUpgrade, SQLiteDatabase.CustomFunction objectRemovedCallback) {
            this(context, name, getDatabaseVersion(context), internal, earlyUpgrade,
                    objectRemovedCallback);
        }

        public DatabaseHelper(Context context, String name, int version, boolean internal,
                boolean earlyUpgrade, SQLiteDatabase.CustomFunction objectRemovedCallback) {
            super(context, name, null, version);
            mContext = context;
            mName = name;
            mVersion = version;
            mInternal = internal;
            mEarlyUpgrade = earlyUpgrade;
            mObjectRemovedCallback = objectRemovedCallback;
            setWriteAheadLoggingEnabled(true);
            setIdleConnectionTimeout(IDLE_CONNECTION_TIMEOUT_MS);
        }

        @Override
        public void onCreate(final SQLiteDatabase db) {
            Log.v(TAG, "onCreate() for " + mName);
            updateDatabase(mContext, db, mInternal, 0, mVersion);
        }

        @Override
        public void onUpgrade(final SQLiteDatabase db, final int oldV, final int newV) {
            Log.v(TAG, "onUpgrade() for " + mName + " from " + oldV + " to " + newV);
            updateDatabase(mContext, db, mInternal, oldV, newV);
        }

        @Override
        public void onDowngrade(final SQLiteDatabase db, final int oldV, final int newV) {
            Log.v(TAG, "onDowngrade() for " + mName + " from " + oldV + " to " + newV);
            downgradeDatabase(mContext, db, mInternal, oldV, newV);
        }

        /**
         * For devices that have removable storage, we support keeping multiple databases
         * to allow users to switch between a number of cards.
         * On such devices, touch this particular database and garbage collect old databases.
         * An LRU cache system is used to clean up databases for old external
         * storage volumes.
         */
        @Override
        public void onOpen(SQLiteDatabase db) {

            if (mEarlyUpgrade) return; // Doing early upgrade.

            if (mObjectRemovedCallback != null) {
                db.addCustomFunction("_OBJECT_REMOVED", 1, mObjectRemovedCallback);
            }

            if (mInternal) return;  // The internal database is kept separately.

            // the code below is only needed on devices with removable storage
            if (!Environment.isExternalStorageRemovable()) return;

            // touch the database file to show it is most recently used
            File file = new File(db.getPath());
            long now = System.currentTimeMillis();
            file.setLastModified(now);

            // delete least recently used databases if we are over the limit
            String[] databases = mContext.databaseList();
            // Don't delete wal auxiliary files(db-shm and db-wal) directly because db file may
            // not be deleted, and it will cause Disk I/O error when accessing this database.
            List<String> dbList = new ArrayList<String>();
            for (String database : databases) {
                if (database != null && database.endsWith(".db")) {
                    dbList.add(database);
                }
            }
            databases = dbList.toArray(new String[0]);
            int count = databases.length;
            int limit = MAX_EXTERNAL_DATABASES;

            // delete external databases that have not been used in the past two months
            long twoMonthsAgo = now - OBSOLETE_DATABASE_DB;
            for (int i = 0; i < databases.length; i++) {
                File other = mContext.getDatabasePath(databases[i]);
                if (INTERNAL_DATABASE_NAME.equals(databases[i]) || file.equals(other)) {
                    databases[i] = null;
                    count--;
                    if (file.equals(other)) {
                        // reduce limit to account for the existence of the database we
                        // are about to open, which we removed from the list.
                        limit--;
                    }
                } else {
                    long time = other.lastModified();
                    if (time < twoMonthsAgo) {
                        if (LOCAL_LOGV) Log.v(TAG, "Deleting old database " + databases[i]);
                        mContext.deleteDatabase(databases[i]);
                        databases[i] = null;
                        count--;
                    }
                }
            }

            // delete least recently used databases until
            // we are no longer over the limit
            while (count > limit) {
                int lruIndex = -1;
                long lruTime = 0;

                for (int i = 0; i < databases.length; i++) {
                    if (databases[i] != null) {
                        long time = mContext.getDatabasePath(databases[i]).lastModified();
                        if (lruTime == 0 || time < lruTime) {
                            lruIndex = i;
                            lruTime = time;
                        }
                    }
                }

                // delete least recently used database
                if (lruIndex != -1) {
                    if (LOCAL_LOGV) Log.v(TAG, "Deleting old database " + databases[lruIndex]);
                    mContext.deleteDatabase(databases[lruIndex]);
                    databases[lruIndex] = null;
                    count--;
                }
            }
        }

        /**
         * List of {@link Uri} that would have been sent directly via
         * {@link ContentResolver#notifyChange}, but are instead being collected
         * due to an ongoing transaction.
         */
        private final ThreadLocal<List<Uri>> mNotifyChanges = new ThreadLocal<>();

        public void beginTransaction() {
            getWritableDatabase().beginTransaction();
            mNotifyChanges.set(new ArrayList<>());
        }

        public void setTransactionSuccessful() {
            getWritableDatabase().setTransactionSuccessful();
            final List<Uri> uris = mNotifyChanges.get();
            if (uris != null) {
                BackgroundThread.getHandler().postDelayed(() -> {
                    for (Uri uri : uris) {
                        notifyChangeInternal(uri);
                    }
                }, sBackgroundDelay);
            }
            mNotifyChanges.remove();
        }

        public void endTransaction() {
            getWritableDatabase().endTransaction();
        }

        /**
         * Notify that the given {@link Uri} has changed. This enqueues the
         * notification if currently inside a transaction, and they'll be
         * clustered and sent when the transaction completes.
         */
        public void notifyChange(Uri uri) {
            if (LOCAL_LOGV) Log.v(TAG, "Notifying " + uri);
            final List<Uri> uris = mNotifyChanges.get();
            if (uris != null) {
                uris.add(uri);
            } else {
                BackgroundThread.getHandler().postDelayed(() -> {
                    notifyChangeInternal(uri);
                }, sBackgroundDelay);
            }
        }

        private void notifyChangeInternal(Uri uri) {
            Trace.traceBegin(TRACE_TAG_DATABASE, "notifyChange");
            try {
                mContext.getContentResolver().notifyChange(uri, null);
            } finally {
                Trace.traceEnd(TRACE_TAG_DATABASE);
            }
        }
    }

    /**
     * Apply {@link Consumer#accept} to the given {@link Uri}.
     * <p>
     * Since media items can be exposed through multiple collections or views,
     * this method expands the single item being accepted to also accept all
     * relevant views.
     */
    public static void acceptWithExpansion(Consumer<Uri> consumer, Uri uri) {
        final int match = matchUri(uri, true);
        acceptWithExpansionInternal(consumer, uri, match);

        try {
            // When targeting a specific volume, we need to expand to also
            // notify the top-level view
            final String volumeName = getVolumeName(uri);
            switch (volumeName) {
                case MediaStore.VOLUME_INTERNAL:
                case MediaStore.VOLUME_EXTERNAL:
                    // Already a top-level view, no need to expand
                    break;
                default:
                    final List<String> segments = new ArrayList<>(uri.getPathSegments());
                    segments.set(0, MediaStore.VOLUME_EXTERNAL);
                    final Uri.Builder builder = uri.buildUpon().path(null);
                    for (String segment : segments) {
                        builder.appendPath(segment);
                    }
                    acceptWithExpansionInternal(consumer, builder.build(), match);
                    break;
            }
        } catch (IllegalArgumentException ignored) {
        }
    }

    private static void acceptWithExpansionInternal(Consumer<Uri> consumer, Uri uri, int match) {
        // Start by always notifying the base item
        consumer.accept(uri);

        // Some items can be exposed through multiple collections,
        // so we need to notify all possible views of those items
        switch (match) {
            case AUDIO_MEDIA_ID:
            case VIDEO_MEDIA_ID:
            case IMAGES_MEDIA_ID: {
                final String volumeName = getVolumeName(uri);
                final long id = ContentUris.parseId(uri);
                consumer.accept(Files.getContentUri(volumeName, id));
                consumer.accept(Downloads.getContentUri(volumeName, id));
                break;
            }
            case AUDIO_MEDIA:
            case VIDEO_MEDIA:
            case IMAGES_MEDIA: {
                final String volumeName = getVolumeName(uri);
                consumer.accept(Files.getContentUri(volumeName));
                consumer.accept(Downloads.getContentUri(volumeName));
                break;
            }
            case FILES_ID:
            case DOWNLOADS_ID: {
                final String volumeName = getVolumeName(uri);
                final long id = ContentUris.parseId(uri);
                consumer.accept(Audio.Media.getContentUri(volumeName, id));
                consumer.accept(Video.Media.getContentUri(volumeName, id));
                consumer.accept(Images.Media.getContentUri(volumeName, id));
                break;
            }
            case FILES:
            case DOWNLOADS: {
                final String volumeName = getVolumeName(uri);
                consumer.accept(Audio.Media.getContentUri(volumeName));
                consumer.accept(Video.Media.getContentUri(volumeName));
                consumer.accept(Images.Media.getContentUri(volumeName));
                break;
            }
        }

        // Any changing audio items mean we probably need to invalidate all
        // indexed views built from that media
        switch (match) {
            case AUDIO_MEDIA:
            case AUDIO_MEDIA_ID: {
                final String volumeName = getVolumeName(uri);
                consumer.accept(Audio.Genres.getContentUri(volumeName));
                consumer.accept(Audio.Playlists.getContentUri(volumeName));
                consumer.accept(Audio.Artists.getContentUri(volumeName));
                consumer.accept(Audio.Albums.getContentUri(volumeName));
                break;
            }
        }
    }

    private static final String[] sDefaultFolderNames = {
        Environment.DIRECTORY_MUSIC,
        Environment.DIRECTORY_PODCASTS,
        Environment.DIRECTORY_RINGTONES,
        Environment.DIRECTORY_ALARMS,
        Environment.DIRECTORY_NOTIFICATIONS,
        Environment.DIRECTORY_PICTURES,
        Environment.DIRECTORY_MOVIES,
        Environment.DIRECTORY_DOWNLOADS,
        Environment.DIRECTORY_DCIM,
    };

    /**
     * This method cleans up any files created by android.media.MiniThumbFile, removed after P.
     * It's triggered during database update only, in order to run only once.
     */
    private static void deleteLegacyThumbnailData() {
        File directory = new File(Environment.getExternalStorageDirectory(), "/DCIM/.thumbnails");

        FilenameFilter filter = (dir, filename) -> filename.startsWith(".thumbdata");
        for (File f : ArrayUtils.defeatNullable(directory.listFiles(filter))) {
            if (!f.delete()) {
                Log.e(TAG, "Failed to delete legacy thumbnail data " + f.getAbsolutePath());
            }
        }
    }

    /**
     * Ensure that default folders are created on mounted primary storage
     * devices. We only do this once per volume so we don't annoy the user if
     * deleted manually.
     */
    private void ensureDefaultFolders(String volumeName, DatabaseHelper helper, SQLiteDatabase db) {
        try {
            final File path = getVolumePath(volumeName);
            final StorageVolume vol = mStorageManager.getStorageVolume(path);
            final String key;
            if (VolumeInfo.ID_EMULATED_INTERNAL.equals(vol.getId())) {
                key = "created_default_folders";
            } else {
                key = "created_default_folders_" + vol.getNormalizedUuid();
            }

            final SharedPreferences prefs = PreferenceManager
                    .getDefaultSharedPreferences(getContext());
            if (prefs.getInt(key, 0) == 0) {
                for (String folderName : sDefaultFolderNames) {
                    final File folder = new File(vol.getPathFile(), folderName);
                    if (!folder.exists()) {
                        folder.mkdirs();
                        insertDirectory(helper, db, folder.getAbsolutePath());
                    }
                }

                SharedPreferences.Editor editor = prefs.edit();
                editor.putInt(key, 1);
                editor.commit();
            }
        } catch (IOException e) {
            Log.w(TAG, "Failed to ensure default folders for " + volumeName, e);
        }
    }

    public static int getDatabaseVersion(Context context) {
        try {
            return context.getPackageManager().getPackageInfo(
                    context.getPackageName(), 0).versionCode;
        } catch (NameNotFoundException e) {
            throw new RuntimeException("couldn't get version code for " + context);
        }
    }

    @Override
    public boolean onCreate() {
        final Context context = getContext();

        // Enable verbose transport logging when requested
        setTransportLoggingEnabled(LOCAL_LOGV);

        // Shift call statistics back to the original caller
        Binder.setProxyTransactListener(
                new Binder.PropagateWorkSourceTransactListener());

        mStorageManager = context.getSystemService(StorageManager.class);
        mAppOpsManager = context.getSystemService(AppOpsManager.class);
        mPackageManager = context.getPackageManager();

        // Reasonable thumbnail size is half of the smallest screen edge width
        final DisplayMetrics metrics = context.getResources().getDisplayMetrics();
        final int thumbSize = Math.min(metrics.widthPixels, metrics.heightPixels) / 2;
        mThumbSize = new Size(thumbSize, thumbSize);

        mInternalDatabase = new DatabaseHelper(context, INTERNAL_DATABASE_NAME, true,
                false, mObjectRemovedCallback);
        mExternalDatabase = new DatabaseHelper(context, EXTERNAL_DATABASE_NAME, false,
                false, mObjectRemovedCallback);

        final IntentFilter filter = new IntentFilter();
        filter.setPriority(10);
        filter.addDataScheme("file");
        filter.addAction(Intent.ACTION_MEDIA_UNMOUNTED);
        filter.addAction(Intent.ACTION_MEDIA_MOUNTED);
        filter.addAction(Intent.ACTION_MEDIA_EJECT);
        filter.addAction(Intent.ACTION_MEDIA_REMOVED);
        filter.addAction(Intent.ACTION_MEDIA_BAD_REMOVAL);
        context.registerReceiver(mMediaReceiver, filter);

        // Watch for invalidation of cached volumes
        mStorageManager.registerListener(new StorageEventListener() {
            @Override
            public void onVolumeStateChanged(VolumeInfo vol, int oldState, int newState) {
                updateVolumes();
            }
        });
        updateVolumes();

        attachVolume(MediaStore.VOLUME_INTERNAL);

        // Attach all currently mounted external volumes
        for (String volumeName : getExternalVolumeNames()) {
            attachVolume(volumeName);
        }

        // Watch for performance-sensitive activity
        mAppOpsManager.startWatchingActive(new int[] {
                AppOpsManager.OP_CAMERA
        }, mActiveListener);

        return true;
    }

    @Override
    public void onCallingPackageChanged() {
        // Identity of the current thread has changed, so invalidate caches
        mCallingIdentity.remove();
    }

    public LocalCallingIdentity clearLocalCallingIdentity() {
        final LocalCallingIdentity token = mCallingIdentity.get();
        mCallingIdentity.set(LocalCallingIdentity.fromSelf());
        return token;
    }

    public void restoreLocalCallingIdentity(LocalCallingIdentity token) {
        mCallingIdentity.set(token);
    }

    public void onIdleMaintenance(@NonNull CancellationSignal signal) {
        final DatabaseHelper helper = mExternalDatabase;
        final SQLiteDatabase db = helper.getReadableDatabase();

        // Scan all volumes to resolve any staleness
        for (String volumeName : getExternalVolumeNames()) {
            // Possibly bail before digging into each volume
            signal.throwIfCanceled();

            try {
                final File file = getVolumePath(volumeName);
                MediaService.onScanVolume(getContext(), Uri.fromFile(file));
            } catch (IOException e) {
                Log.w(TAG, e);
            }
        }

        // Delete any stale thumbnails
        pruneThumbnails(signal);

        // Finished orphaning any content whose package no longer exists
        final ArraySet<String> unknownPackages = new ArraySet<>();
        try (Cursor c = db.query(true, "files", new String[] { "owner_package_name" },
                null, null, null, null, null, null, signal)) {
            while (c.moveToNext()) {
                final String packageName = c.getString(0);
                if (TextUtils.isEmpty(packageName)) continue;
                try {
                    getContext().getPackageManager().getPackageInfo(packageName,
                            PackageManager.MATCH_UNINSTALLED_PACKAGES);
                } catch (NameNotFoundException e) {
                    unknownPackages.add(packageName);
                }
            }
        }

        Log.d(TAG, "Found " + unknownPackages.size() + " unknown packages");
        for (String packageName : unknownPackages) {
            onPackageOrphaned(packageName);
        }

        // Delete any expired content; we're paranoid about wildly changing
        // clocks, so only delete items within the last week
        final long from = ((System.currentTimeMillis() - DateUtils.WEEK_IN_MILLIS) / 1000);
        final long to = (System.currentTimeMillis() / 1000);
        try (Cursor c = db.query(true, "files", new String[] { "volume_name", "_id" },
                FileColumns.DATE_EXPIRES + " BETWEEN " + from + " AND " + to, null,
                null, null, null, null, signal)) {
            while (c.moveToNext()) {
                final String volumeName = c.getString(0);
                final long id = c.getLong(1);
                delete(Files.getContentUri(volumeName, id), null, null);
            }
            Log.d(TAG, "Deleted " + c.getCount() + " expired items on " + helper.mName);
        }

        // Forget any stale volumes
        final long lastWeek = System.currentTimeMillis() - DateUtils.WEEK_IN_MILLIS;
        for (VolumeRecord rec : mStorageManager.getVolumeRecords()) {
            // Skip volumes without valid UUIDs
            if (TextUtils.isEmpty(rec.fsUuid)) continue;

            // Skip volumes that are currently mounted
            final VolumeInfo vol = mStorageManager.findVolumeByUuid(rec.fsUuid);
            if (vol != null && vol.isMountedReadable()) continue;

            if (rec.lastSeenMillis > 0 && rec.lastSeenMillis < lastWeek) {
                final int num = db.delete("files", FileColumns.VOLUME_NAME + "=?",
                        new String[] { rec.getNormalizedFsUuid() });
                Log.d(TAG, "Forgot " + num + " stale items from " + rec.fsUuid);
            }
        }
    }

    public void onPackageOrphaned(String packageName) {
        final DatabaseHelper helper = mExternalDatabase;
        final SQLiteDatabase db = helper.getWritableDatabase();

        final ContentValues values = new ContentValues();
        values.putNull(FileColumns.OWNER_PACKAGE_NAME);

        final int count = db.update("files", values,
                "owner_package_name=?", new String[] { packageName });
        if (count > 0) {
            Log.d(TAG, "Orphaned " + count + " items belonging to "
                    + packageName + " on " + helper.mName);
        }
    }

    private void enforceShellRestrictions() {
        if (UserHandle.getCallingAppId() == android.os.Process.SHELL_UID
                && getContext().getSystemService(UserManager.class)
                        .hasUserRestriction(UserManager.DISALLOW_USB_FILE_TRANSFER)) {
            throw new SecurityException(
                    "Shell user cannot access files for user " + UserHandle.myUserId());
        }
    }

    @Override
    protected int enforceReadPermissionInner(Uri uri, String callingPkg, IBinder callerToken)
            throws SecurityException {
        enforceShellRestrictions();
        return super.enforceReadPermissionInner(uri, callingPkg, callerToken);
    }

    @Override
    protected int enforceWritePermissionInner(Uri uri, String callingPkg, IBinder callerToken)
            throws SecurityException {
        enforceShellRestrictions();
        return super.enforceWritePermissionInner(uri, callingPkg, callerToken);
    }

    @VisibleForTesting
    static void makePristineSchema(SQLiteDatabase db) {
        // drop all triggers
        Cursor c = db.query("sqlite_master", new String[] {"name"}, "type is 'trigger'",
                null, null, null, null);
        while (c.moveToNext()) {
            if (c.getString(0).startsWith("sqlite_")) continue;
            db.execSQL("DROP TRIGGER IF EXISTS " + c.getString(0));
        }
        c.close();

        // drop all views
        c = db.query("sqlite_master", new String[] {"name"}, "type is 'view'",
                null, null, null, null);
        while (c.moveToNext()) {
            if (c.getString(0).startsWith("sqlite_")) continue;
            db.execSQL("DROP VIEW IF EXISTS " + c.getString(0));
        }
        c.close();

        // drop all indexes
        c = db.query("sqlite_master", new String[] {"name"}, "type is 'index'",
                null, null, null, null);
        while (c.moveToNext()) {
            if (c.getString(0).startsWith("sqlite_")) continue;
            db.execSQL("DROP INDEX IF EXISTS " + c.getString(0));
        }
        c.close();

        // drop all tables
        c = db.query("sqlite_master", new String[] {"name"}, "type is 'table'",
                null, null, null, null);
        while (c.moveToNext()) {
            if (c.getString(0).startsWith("sqlite_")) continue;
            db.execSQL("DROP TABLE IF EXISTS " + c.getString(0));
        }
        c.close();
    }

    private static void createLatestSchema(SQLiteDatabase db, boolean internal) {
        // We're about to start all ID numbering from scratch, so revoke any
        // outstanding permission grants to ensure we don't leak data
        AppGlobals.getInitialApplication().revokeUriPermission(MediaStore.AUTHORITY_URI,
                Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
        MediaDocumentsProvider.revokeAllUriGrants(AppGlobals.getInitialApplication());
        BackgroundThread.getHandler().post(() -> {
            try (ContentProviderClient client = AppGlobals.getInitialApplication()
                    .getContentResolver().acquireContentProviderClient(
                            android.provider.Downloads.Impl.AUTHORITY)) {
                client.call(android.provider.Downloads.CALL_REVOKE_MEDIASTORE_URI_PERMS,
                        null, null);
            } catch (RemoteException e) {
                // Should not happen
            }
        });

        makePristineSchema(db);

        db.execSQL("CREATE TABLE android_metadata (locale TEXT)");
        db.execSQL("CREATE TABLE thumbnails (_id INTEGER PRIMARY KEY,_data TEXT,image_id INTEGER,"
                + "kind INTEGER,width INTEGER,height INTEGER)");
        db.execSQL("CREATE TABLE artists (artist_id INTEGER PRIMARY KEY,"
                + "artist_key TEXT NOT NULL UNIQUE,artist TEXT NOT NULL)");
        db.execSQL("CREATE TABLE albums (album_id INTEGER PRIMARY KEY,"
                + "album_key TEXT NOT NULL UNIQUE,album TEXT NOT NULL)");
        db.execSQL("CREATE TABLE album_art (album_id INTEGER PRIMARY KEY,_data TEXT)");
        db.execSQL("CREATE TABLE videothumbnails (_id INTEGER PRIMARY KEY,_data TEXT,"
                + "video_id INTEGER,kind INTEGER,width INTEGER,height INTEGER)");
        db.execSQL("CREATE TABLE files (_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                + "_data TEXT UNIQUE COLLATE NOCASE,_size INTEGER,format INTEGER,parent INTEGER,"
                + "date_added INTEGER,date_modified INTEGER,mime_type TEXT,title TEXT,"
                + "description TEXT,_display_name TEXT,picasa_id TEXT,orientation INTEGER,"
                + "latitude DOUBLE,longitude DOUBLE,datetaken INTEGER,mini_thumb_magic INTEGER,"
                + "bucket_id TEXT,bucket_display_name TEXT,isprivate INTEGER,title_key TEXT,"
                + "artist_id INTEGER,album_id INTEGER,composer TEXT,track INTEGER,"
                + "year INTEGER CHECK(year!=0),is_ringtone INTEGER,is_music INTEGER,"
                + "is_alarm INTEGER,is_notification INTEGER,is_podcast INTEGER,album_artist TEXT,"
                + "duration INTEGER,bookmark INTEGER,artist TEXT,album TEXT,resolution TEXT,"
                + "tags TEXT,category TEXT,language TEXT,mini_thumb_data TEXT,name TEXT,"
                + "media_type INTEGER,old_id INTEGER,is_drm INTEGER,"
                + "width INTEGER, height INTEGER, title_resource_uri TEXT,"
                + "owner_package_name TEXT DEFAULT NULL,"
                + "color_standard INTEGER, color_transfer INTEGER, color_range INTEGER,"
                + "_hash BLOB DEFAULT NULL, is_pending INTEGER DEFAULT 0,"
                + "is_download INTEGER DEFAULT 0, download_uri TEXT DEFAULT NULL,"
                + "referer_uri TEXT DEFAULT NULL, is_audiobook INTEGER DEFAULT 0,"
                + "date_expires INTEGER DEFAULT NULL,is_trashed INTEGER DEFAULT 0,"
                + "group_id INTEGER DEFAULT NULL,primary_directory TEXT DEFAULT NULL,"
                + "secondary_directory TEXT DEFAULT NULL,document_id TEXT DEFAULT NULL,"
                + "instance_id TEXT DEFAULT NULL,original_document_id TEXT DEFAULT NULL,"
                + "relative_path TEXT DEFAULT NULL,volume_name TEXT DEFAULT NULL)");

        db.execSQL("CREATE TABLE log (time DATETIME, message TEXT)");
        if (!internal) {
            db.execSQL("CREATE TABLE audio_genres (_id INTEGER PRIMARY KEY,name TEXT NOT NULL)");
            db.execSQL("CREATE TABLE audio_genres_map (_id INTEGER PRIMARY KEY,"
                    + "audio_id INTEGER NOT NULL,genre_id INTEGER NOT NULL,"
                    + "UNIQUE (audio_id,genre_id) ON CONFLICT IGNORE)");
            db.execSQL("CREATE TABLE audio_playlists_map (_id INTEGER PRIMARY KEY,"
                    + "audio_id INTEGER NOT NULL,playlist_id INTEGER NOT NULL,"
                    + "play_order INTEGER NOT NULL)");
            db.execSQL("CREATE TRIGGER audio_genres_cleanup DELETE ON audio_genres BEGIN DELETE"
                    + " FROM audio_genres_map WHERE genre_id = old._id;END");
            db.execSQL("CREATE TRIGGER audio_playlists_cleanup DELETE ON files"
                    + " WHEN old.media_type=4"
                    + " BEGIN DELETE FROM audio_playlists_map WHERE playlist_id = old._id;"
                    + "SELECT _DELETE_FILE(old._data);END");
            db.execSQL("CREATE TRIGGER files_cleanup DELETE ON files"
                    + " BEGIN SELECT _OBJECT_REMOVED(old._id);END");
        }

        db.execSQL("CREATE INDEX image_id_index on thumbnails(image_id)");
        db.execSQL("CREATE INDEX album_idx on albums(album)");
        db.execSQL("CREATE INDEX albumkey_index on albums(album_key)");
        db.execSQL("CREATE INDEX artist_idx on artists(artist)");
        db.execSQL("CREATE INDEX artistkey_index on artists(artist_key)");
        db.execSQL("CREATE INDEX video_id_index on videothumbnails(video_id)");
        db.execSQL("CREATE INDEX album_id_idx ON files(album_id)");
        db.execSQL("CREATE INDEX artist_id_idx ON files(artist_id)");
        db.execSQL("CREATE INDEX bucket_index on files(bucket_id,media_type,datetaken, _id)");
        db.execSQL("CREATE INDEX bucket_name on files(bucket_id,media_type,bucket_display_name)");
        db.execSQL("CREATE INDEX format_index ON files(format)");
        db.execSQL("CREATE INDEX media_type_index ON files(media_type)");
        db.execSQL("CREATE INDEX parent_index ON files(parent)");
        db.execSQL("CREATE INDEX path_index ON files(_data)");
        db.execSQL("CREATE INDEX sort_index ON files(datetaken ASC, _id ASC)");
        db.execSQL("CREATE INDEX title_idx ON files(title)");
        db.execSQL("CREATE INDEX titlekey_index ON files(title_key)");

        db.execSQL("CREATE TRIGGER albumart_cleanup1 DELETE ON albums BEGIN DELETE FROM album_art"
                + " WHERE album_id = old.album_id;END");
        db.execSQL("CREATE TRIGGER albumart_cleanup2 DELETE ON album_art"
                + " BEGIN SELECT _DELETE_FILE(old._data);END");

        createLatestViews(db, internal);
    }

    private static void makePristineViews(SQLiteDatabase db) {
        // drop all views
        Cursor c = db.query("sqlite_master", new String[] {"name"}, "type is 'view'",
                null, null, null, null);
        while (c.moveToNext()) {
            db.execSQL("DROP VIEW IF EXISTS " + c.getString(0));
        }
        c.close();
    }

    private static void createLatestViews(SQLiteDatabase db, boolean internal) {
        makePristineViews(db);

        if (!internal) {
            db.execSQL("CREATE VIEW audio_playlists AS SELECT _id,_data,name,date_added,"
                    + "date_modified,owner_package_name,_hash,is_pending,date_expires,is_trashed,"
                    + "volume_name FROM files WHERE media_type=4");
        }

        db.execSQL("CREATE VIEW audio_meta AS SELECT _id,_data,_display_name,_size,mime_type,"
                + "date_added,is_drm,date_modified,title,title_key,duration,artist_id,composer,"
                + "album_id,track,year,is_ringtone,is_music,is_alarm,is_notification,is_podcast,"
                + "bookmark,album_artist,owner_package_name,_hash,is_pending,is_audiobook,"
                + "date_expires,is_trashed,group_id,primary_directory,secondary_directory,"
                + "document_id,instance_id,original_document_id,title_resource_uri,relative_path,"
                + "volume_name,datetaken,bucket_id,bucket_display_name,group_id,orientation"
                + " FROM files WHERE media_type=2");

        db.execSQL("CREATE VIEW artists_albums_map AS SELECT DISTINCT artist_id, album_id"
                + " FROM audio_meta");
        db.execSQL("CREATE VIEW audio as SELECT *, NULL AS width, NULL as height"
                + " FROM audio_meta LEFT OUTER JOIN artists"
                + " ON audio_meta.artist_id=artists.artist_id LEFT OUTER JOIN albums"
                + " ON audio_meta.album_id=albums.album_id");
        db.execSQL("CREATE VIEW album_info AS SELECT audio.album_id AS _id, album, album_key,"
                + " MIN(year) AS minyear, MAX(year) AS maxyear, artist, artist_id, artist_key,"
                + " count(*) AS numsongs,album_art._data AS album_art FROM audio"
                + " LEFT OUTER JOIN album_art ON audio.album_id=album_art.album_id WHERE is_music=1"
                + " GROUP BY audio.album_id");
        db.execSQL("CREATE VIEW searchhelpertitle AS SELECT * FROM audio ORDER BY title_key");
        db.execSQL("CREATE VIEW artist_info AS SELECT artist_id AS _id, artist, artist_key,"
                + " COUNT(DISTINCT album_key) AS number_of_albums, COUNT(*) AS number_of_tracks"
                + " FROM audio"
                + " WHERE is_music=1 GROUP BY artist_key");
        db.execSQL("CREATE VIEW search AS SELECT _id,'artist' AS mime_type,artist,NULL AS album,"
                + "NULL AS title,artist AS text1,NULL AS text2,number_of_albums AS data1,"
                + "number_of_tracks AS data2,artist_key AS match,"
                + "'content://media/external/audio/artists/'||_id AS suggest_intent_data,"
                + "1 AS grouporder FROM artist_info WHERE (artist!='<unknown>')"
                + " UNION ALL SELECT _id,'album' AS mime_type,artist,album,"
                + "NULL AS title,album AS text1,artist AS text2,NULL AS data1,"
                + "NULL AS data2,artist_key||' '||album_key AS match,"
                + "'content://media/external/audio/albums/'||_id AS suggest_intent_data,"
                + "2 AS grouporder FROM album_info"
                + " WHERE (album!='<unknown>')"
                + " UNION ALL SELECT searchhelpertitle._id AS _id,mime_type,artist,album,title,"
                + "title AS text1,artist AS text2,NULL AS data1,"
                + "NULL AS data2,artist_key||' '||album_key||' '||title_key AS match,"
                + "'content://media/external/audio/media/'||searchhelpertitle._id"
                + " AS suggest_intent_data,"
                + "3 AS grouporder FROM searchhelpertitle WHERE (title != '')");
        db.execSQL("CREATE VIEW audio_genres_map_noid AS SELECT audio_id,genre_id"
                + " FROM audio_genres_map");

        db.execSQL("CREATE VIEW video AS SELECT "
                + String.join(",", getProjectionMap(Video.Media.class).keySet())
                + " FROM files WHERE media_type=3");
        db.execSQL("CREATE VIEW images AS SELECT "
                + String.join(",", getProjectionMap(Images.Media.class).keySet())
                + " FROM files WHERE media_type=1");
        db.execSQL("CREATE VIEW downloads AS SELECT "
                + String.join(",", getProjectionMap(Downloads.class).keySet())
                + " FROM files WHERE is_download=1");
    }

    private static void updateCollationKeys(SQLiteDatabase db) {
        // Delete albums and artists, then clear the modification time on songs, which
        // will cause the media scanner to rescan everything, rebuilding the artist and
        // album tables along the way, while preserving playlists.
        // We need this rescan because ICU also changed, and now generates different
        // collation keys
        db.execSQL("DELETE from albums");
        db.execSQL("DELETE from artists");
        db.execSQL("UPDATE files SET date_modified=0;");
    }

    private static void updateAddTitleResource(SQLiteDatabase db) {
        // Add the column used for title localization, and force a rescan of any
        // ringtones, alarms and notifications that may be using it.
        db.execSQL("ALTER TABLE files ADD COLUMN title_resource_uri TEXT");
        db.execSQL("UPDATE files SET date_modified=0"
                + " WHERE (is_alarm IS 1) OR (is_ringtone IS 1) OR (is_notification IS 1)");
    }

    private static void updateAddOwnerPackageName(SQLiteDatabase db, boolean internal) {
        db.execSQL("ALTER TABLE files ADD COLUMN owner_package_name TEXT DEFAULT NULL");

        // Derive new column value based on well-known paths
        try (Cursor c = db.query("files", new String[] { FileColumns._ID, FileColumns.DATA },
                FileColumns.DATA + " REGEXP '" + PATTERN_OWNED_PATH.pattern() + "'",
                null, null, null, null, null)) {
            Log.d(TAG, "Updating " + c.getCount() + " entries with well-known owners");

            final Matcher m = PATTERN_OWNED_PATH.matcher("");
            final ContentValues values = new ContentValues();

            while (c.moveToNext()) {
                final long id = c.getLong(0);
                final String data = c.getString(1);
                m.reset(data);
                if (m.matches()) {
                    final String packageName = m.group(1);
                    values.clear();
                    values.put(FileColumns.OWNER_PACKAGE_NAME, packageName);
                    db.update("files", values, "_id=" + id, null);
                }
            }
        }
    }

    private static void updateAddColorSpaces(SQLiteDatabase db) {
        // Add the color aspects related column used for HDR detection etc.
        db.execSQL("ALTER TABLE files ADD COLUMN color_standard INTEGER;");
        db.execSQL("ALTER TABLE files ADD COLUMN color_transfer INTEGER;");
        db.execSQL("ALTER TABLE files ADD COLUMN color_range INTEGER;");
    }

    private static void updateAddHashAndPending(SQLiteDatabase db, boolean internal) {
        db.execSQL("ALTER TABLE files ADD COLUMN _hash BLOB DEFAULT NULL;");
        db.execSQL("ALTER TABLE files ADD COLUMN is_pending INTEGER DEFAULT 0;");
    }

    private static void updateAddDownloadInfo(SQLiteDatabase db, boolean internal) {
        db.execSQL("ALTER TABLE files ADD COLUMN is_download INTEGER DEFAULT 0;");
        db.execSQL("ALTER TABLE files ADD COLUMN download_uri TEXT DEFAULT NULL;");
        db.execSQL("ALTER TABLE files ADD COLUMN referer_uri TEXT DEFAULT NULL;");
    }

    private static void updateAddAudiobook(SQLiteDatabase db, boolean internal) {
        db.execSQL("ALTER TABLE files ADD COLUMN is_audiobook INTEGER DEFAULT 0;");
    }

    private static void updateClearLocation(SQLiteDatabase db, boolean internal) {
        db.execSQL("UPDATE files SET latitude=NULL, longitude=NULL;");
    }

    private static void updateSetIsDownload(SQLiteDatabase db, boolean internal) {
        db.execSQL("UPDATE files SET is_download=1 WHERE _data REGEXP '"
                + PATTERN_DOWNLOADS_FILE + "'");
    }

    private static void updateAddExpiresAndTrashed(SQLiteDatabase db, boolean internal) {
        db.execSQL("ALTER TABLE files ADD COLUMN date_expires INTEGER DEFAULT NULL;");
        db.execSQL("ALTER TABLE files ADD COLUMN is_trashed INTEGER DEFAULT 0;");
    }

    private static void updateAddGroupId(SQLiteDatabase db, boolean internal) {
        db.execSQL("ALTER TABLE files ADD COLUMN group_id INTEGER DEFAULT NULL;");
    }

    private static void updateAddDirectories(SQLiteDatabase db, boolean internal) {
        db.execSQL("ALTER TABLE files ADD COLUMN primary_directory TEXT DEFAULT NULL;");
        db.execSQL("ALTER TABLE files ADD COLUMN secondary_directory TEXT DEFAULT NULL;");
    }

    private static void updateAddXmp(SQLiteDatabase db, boolean internal) {
        db.execSQL("ALTER TABLE files ADD COLUMN document_id TEXT DEFAULT NULL;");
        db.execSQL("ALTER TABLE files ADD COLUMN instance_id TEXT DEFAULT NULL;");
        db.execSQL("ALTER TABLE files ADD COLUMN original_document_id TEXT DEFAULT NULL;");
    }

    private static void updateAddPath(SQLiteDatabase db, boolean internal) {
        db.execSQL("ALTER TABLE files ADD COLUMN relative_path TEXT DEFAULT NULL;");
    }

    private static void updateAddVolumeName(SQLiteDatabase db, boolean internal) {
        db.execSQL("ALTER TABLE files ADD COLUMN volume_name TEXT DEFAULT NULL;");
    }

    private static void updateDirsMimeType(SQLiteDatabase db, boolean internal) {
        db.execSQL("UPDATE files SET mime_type=NULL WHERE format="
                + MtpConstants.FORMAT_ASSOCIATION);
    }

    private static void updateRelativePath(SQLiteDatabase db, boolean internal) {
        db.execSQL("UPDATE files"
                + " SET " + MediaColumns.RELATIVE_PATH + "=" + MediaColumns.RELATIVE_PATH + "||'/'"
                + " WHERE " + MediaColumns.RELATIVE_PATH + " IS NOT NULL"
                + " AND " + MediaColumns.RELATIVE_PATH + " NOT LIKE '%/';");
    }

    private static void recomputeDataValues(SQLiteDatabase db, boolean internal) {
        try (Cursor c = db.query("files", new String[] { FileColumns._ID, FileColumns.DATA },
                null, null, null, null, null, null)) {
            Log.d(TAG, "Recomputing " + c.getCount() + " data values");

            final ContentValues values = new ContentValues();
            while (c.moveToNext()) {
                values.clear();
                final long id = c.getLong(0);
                final String data = c.getString(1);
                values.put(FileColumns.DATA, data);
                computeDataValues(values);
                values.remove(FileColumns.DATA);
                if (!values.isEmpty()) {
                    db.update("files", values, "_id=" + id, null);
                }
            }
        }
    }

    static final int VERSION_J = 509;
    static final int VERSION_K = 700;
    static final int VERSION_L = 700;
    static final int VERSION_M = 800;
    static final int VERSION_N = 800;
    static final int VERSION_O = 800;
    static final int VERSION_P = 900;
    static final int VERSION_Q = 1023;

    /**
     * This method takes care of updating all the tables in the database to the
     * current version, creating them if necessary.
     * This method can only update databases at schema 700 or higher, which was
     * used by the KitKat release. Older database will be cleared and recreated.
     * @param db Database
     * @param internal True if this is the internal media database
     */
    private static void updateDatabase(Context context, SQLiteDatabase db, boolean internal,
            int fromVersion, int toVersion) {
        final long startTime = SystemClock.elapsedRealtime();

        if (fromVersion < 700) {
            // Anything older than KK is recreated from scratch
            createLatestSchema(db, internal);
        } else {
            boolean recomputeDataValues = false;
            if (fromVersion < 800) {
                updateCollationKeys(db);
            }
            if (fromVersion < 900) {
                updateAddTitleResource(db);
            }
            if (fromVersion < 1000) {
                updateAddOwnerPackageName(db, internal);
            }
            if (fromVersion < 1003) {
                updateAddColorSpaces(db);
            }
            if (fromVersion < 1004) {
                updateAddHashAndPending(db, internal);
            }
            if (fromVersion < 1005) {
                updateAddDownloadInfo(db, internal);
            }
            if (fromVersion < 1006) {
                updateAddAudiobook(db, internal);
            }
            if (fromVersion < 1007) {
                updateClearLocation(db, internal);
            }
            if (fromVersion < 1008) {
                updateSetIsDownload(db, internal);
            }
            if (fromVersion < 1009) {
                // This database version added "secondary_bucket_id", but that
                // column name was refactored in version 1013 below, so this
                // update step is no longer needed.
            }
            if (fromVersion < 1010) {
                updateAddExpiresAndTrashed(db, internal);
            }
            if (fromVersion < 1012) {
                recomputeDataValues = true;
            }
            if (fromVersion < 1013) {
                updateAddGroupId(db, internal);
                updateAddDirectories(db, internal);
                recomputeDataValues = true;
            }
            if (fromVersion < 1014) {
                updateAddXmp(db, internal);
            }
            if (fromVersion < 1015) {
                // Empty version bump to ensure views are recreated
            }
            if (fromVersion < 1016) {
                // Empty version bump to ensure views are recreated
            }
            if (fromVersion < 1017) {
                updateSetIsDownload(db, internal);
                recomputeDataValues = true;
            }
            if (fromVersion < 1018) {
                updateAddPath(db, internal);
                recomputeDataValues = true;
            }
            if (fromVersion < 1019) {
                // Only trigger during "external", so that it runs only once.
                if (!internal) {
                    deleteLegacyThumbnailData();
                }
            }
            if (fromVersion < 1020) {
                updateAddVolumeName(db, internal);
                recomputeDataValues = true;
            }
            if (fromVersion < 1021) {
                // Empty version bump to ensure views are recreated
            }
            if (fromVersion < 1022) {
                updateDirsMimeType(db, internal);
            }
            if (fromVersion < 1023) {
                updateRelativePath(db, internal);
            }

            if (recomputeDataValues) {
                recomputeDataValues(db, internal);
            }
        }

        // Always recreate latest views during upgrade; they're cheap and it's
        // an easy way to ensure they're defined consistently
        createLatestViews(db, internal);

        sanityCheck(db, fromVersion);

        getOrCreateUuid(db);

        final long elapsedSeconds = (SystemClock.elapsedRealtime() - startTime)
                / DateUtils.SECOND_IN_MILLIS;
        logToDb(db, "Database upgraded from version " + fromVersion + " to " + toVersion
                + " in " + elapsedSeconds + " seconds");
    }

    private static void downgradeDatabase(Context context, SQLiteDatabase db, boolean internal,
            int fromVersion, int toVersion) {
        final long startTime = SystemClock.elapsedRealtime();

        // The best we can do is wipe and start over
        createLatestSchema(db, internal);

        final long elapsedSeconds = (SystemClock.elapsedRealtime() - startTime)
                / DateUtils.SECOND_IN_MILLIS;
        logToDb(db, "Database downgraded from version " + fromVersion + " to " + toVersion
                + " in " + elapsedSeconds + " seconds");
    }

    /**
     * Write a persistent diagnostic message to the log table.
     */
    static void logToDb(SQLiteDatabase db, String message) {
        db.execSQL("INSERT OR REPLACE" +
                " INTO log (time,message) VALUES (strftime('%Y-%m-%d %H:%M:%f','now'),?);",
                new String[] { message });
        // delete all but the last 500 rows
        db.execSQL("DELETE FROM log WHERE rowid IN" +
                " (SELECT rowid FROM log ORDER BY rowid DESC LIMIT 500,-1);");
    }

    /**
     * Perform a simple sanity check on the database. Currently this tests
     * whether all the _data entries in audio_meta are unique
     */
    private static void sanityCheck(SQLiteDatabase db, int fromVersion) {
        Cursor c1 = null;
        Cursor c2 = null;
        try {
            c1 = db.query("audio_meta", new String[] {"count(*)"},
                    null, null, null, null, null);
            c2 = db.query("audio_meta", new String[] {"count(distinct _data)"},
                    null, null, null, null, null);
            c1.moveToFirst();
            c2.moveToFirst();
            int num1 = c1.getInt(0);
            int num2 = c2.getInt(0);
            if (num1 != num2) {
                Log.e(TAG, "audio_meta._data column is not unique while upgrading" +
                        " from schema " +fromVersion + " : " + num1 +"/" + num2);
                // Delete all audio_meta rows so they will be rebuilt by the media scanner
                db.execSQL("DELETE FROM audio_meta;");
            }
        } finally {
            IoUtils.closeQuietly(c1);
            IoUtils.closeQuietly(c2);
        }
    }

    private static final String XATTR_UUID = "user.uuid";

    /**
     * Return a UUID for the given database. If the database is deleted or
     * otherwise corrupted, then a new UUID will automatically be generated.
     */
    private static @NonNull String getOrCreateUuid(@NonNull SQLiteDatabase db) {
        try {
            return new String(Os.getxattr(db.getPath(), XATTR_UUID));
        } catch (ErrnoException e) {
            if (e.errno == OsConstants.ENODATA) {
                // Doesn't exist yet, so generate and persist a UUID
                final String uuid = UUID.randomUUID().toString();
                try {
                    Os.setxattr(db.getPath(), XATTR_UUID, uuid.getBytes(), 0);
                } catch (ErrnoException e2) {
                    throw new RuntimeException(e);
                }
                return uuid;
            } else {
                throw new RuntimeException(e);
            }
        }
    }

    @VisibleForTesting
    static void computeDataValues(ContentValues values) {
        // Worst case we have to assume no bucket details
        values.remove(ImageColumns.BUCKET_ID);
        values.remove(ImageColumns.BUCKET_DISPLAY_NAME);
        values.remove(ImageColumns.GROUP_ID);
        values.remove(ImageColumns.VOLUME_NAME);
        values.remove(ImageColumns.RELATIVE_PATH);
        values.remove(ImageColumns.PRIMARY_DIRECTORY);
        values.remove(ImageColumns.SECONDARY_DIRECTORY);

        final String data = values.getAsString(MediaColumns.DATA);
        if (TextUtils.isEmpty(data)) return;

        final File file = new File(data);
        final File fileLower = new File(data.toLowerCase());

        values.put(ImageColumns.VOLUME_NAME, extractVolumeName(data));
        values.put(ImageColumns.RELATIVE_PATH, extractRelativePath(data));
        values.put(ImageColumns.DISPLAY_NAME, extractDisplayName(data));

        // Buckets are the parent directory
        final String parent = fileLower.getParent();
        if (parent != null) {
            values.put(ImageColumns.BUCKET_ID, parent.hashCode());
            // The relative path for files in the top directory is "/"
            if (!"/".equals(values.getAsString(ImageColumns.RELATIVE_PATH))) {
                values.put(ImageColumns.BUCKET_DISPLAY_NAME, file.getParentFile().getName());
            }
        }

        // Groups are the first part of name
        final String name = fileLower.getName();
        final int firstDot = name.indexOf('.');
        if (firstDot > 0) {
            values.put(ImageColumns.GROUP_ID,
                    name.substring(0, firstDot).hashCode());
        }

        // Directories are first two levels of storage paths
        final String relativePath = values.getAsString(ImageColumns.RELATIVE_PATH);
        if (TextUtils.isEmpty(relativePath)) return;

        final String[] segments = relativePath.split("/");
        if (segments.length > 0) {
            values.put(ImageColumns.PRIMARY_DIRECTORY, segments[0]);
        }
        if (segments.length > 1) {
            values.put(ImageColumns.SECONDARY_DIRECTORY, segments[1]);
        }
    }

    @Override
    public Uri canonicalize(Uri uri) {
        final boolean allowHidden = isCallingPackageAllowedHidden();
        final int match = matchUri(uri, allowHidden);

        // Skip when we have nothing to canonicalize
        if ("1".equals(uri.getQueryParameter(CANONICAL))) {
            return uri;
        }

        try (Cursor c = queryForSingleItem(uri, null, null, null, null)) {
            switch (match) {
                case AUDIO_MEDIA_ID: {
                    final String title = getDefaultTitleFromCursor(c);
                    if (!TextUtils.isEmpty(title)) {
                        final Uri.Builder builder = uri.buildUpon();
                        builder.appendQueryParameter(AudioColumns.TITLE, title);
                        builder.appendQueryParameter(CANONICAL, "1");
                        return builder.build();
                    }
                }
                case VIDEO_MEDIA_ID:
                case IMAGES_MEDIA_ID: {
                    final String documentId = c
                            .getString(c.getColumnIndexOrThrow(MediaColumns.DOCUMENT_ID));
                    if (!TextUtils.isEmpty(documentId)) {
                        final Uri.Builder builder = uri.buildUpon();
                        builder.appendQueryParameter(MediaColumns.DOCUMENT_ID, documentId);
                        builder.appendQueryParameter(CANONICAL, "1");
                        return builder.build();
                    }
                }
            }
        } catch (FileNotFoundException e) {
            Log.w(TAG, e.getMessage());
        }
        return null;
    }

    @Override
    public Uri uncanonicalize(Uri uri) {
        final boolean allowHidden = isCallingPackageAllowedHidden();
        final int match = matchUri(uri, allowHidden);

        // Skip when we have nothing to uncanonicalize
        if (!"1".equals(uri.getQueryParameter(CANONICAL))) {
            return uri;
        }

        // Extract values and then clear to avoid recursive lookups
        final String title = uri.getQueryParameter(AudioColumns.TITLE);
        final String documentId = uri.getQueryParameter(MediaColumns.DOCUMENT_ID);
        uri = uri.buildUpon().clearQuery().build();

        switch (match) {
            case AUDIO_MEDIA_ID: {
                // First check for an exact match
                try (Cursor c = queryForSingleItem(uri, null, null, null, null)) {
                    if (Objects.equals(title, getDefaultTitleFromCursor(c))) {
                        return uri;
                    }
                } catch (FileNotFoundException e) {
                    Log.w(TAG, "Trouble resolving " + uri + "; falling back to search: " + e);
                }

                // Otherwise fallback to searching
                final Uri baseUri = ContentUris.removeId(uri);
                try (Cursor c = queryForSingleItem(baseUri,
                        new String[] { BaseColumns._ID },
                        AudioColumns.TITLE + "=?", new String[] { title }, null)) {
                    return ContentUris.withAppendedId(baseUri, c.getLong(0));
                } catch (FileNotFoundException e) {
                    Log.w(TAG, "Failed to resolve " + uri + ": " + e);
                    return null;
                }
            }
            case VIDEO_MEDIA_ID:
            case IMAGES_MEDIA_ID: {
                // First check for an exact match
                try (Cursor c = queryForSingleItem(uri, null, null, null, null)) {
                    if (Objects.equals(title, getDefaultTitleFromCursor(c))) {
                        return uri;
                    }
                } catch (FileNotFoundException e) {
                    Log.w(TAG, "Trouble resolving " + uri + "; falling back to search: " + e);
                }

                // Otherwise fallback to searching
                final Uri baseUri = ContentUris.removeId(uri);
                try (Cursor c = queryForSingleItem(baseUri,
                        new String[] { BaseColumns._ID },
                        MediaColumns.DOCUMENT_ID + "=?", new String[] { documentId }, null)) {
                    return ContentUris.withAppendedId(baseUri, c.getLong(0));
                } catch (FileNotFoundException e) {
                    Log.w(TAG, "Failed to resolve " + uri + ": " + e);
                    return null;
                }
            }
        }

        return uri;
    }

    private Uri safeUncanonicalize(Uri uri) {
        Uri newUri = uncanonicalize(uri);
        if (newUri != null) {
            return newUri;
        }
        return uri;
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs,
            String sortOrder) {
        return query(uri, projection,
                ContentResolver.createSqlQueryBundle(selection, selectionArgs, sortOrder), null);
    }

    @Override
    public Cursor query(Uri uri, String[] projection, Bundle queryArgs, CancellationSignal signal) {
        Trace.traceBegin(TRACE_TAG_DATABASE, "query");
        try {
            return queryInternal(uri, projection, queryArgs, signal);
        } finally {
            Trace.traceEnd(TRACE_TAG_DATABASE);
        }
    }

    private Cursor queryInternal(Uri uri, String[] projection, Bundle queryArgs,
            CancellationSignal signal) {
        String selection = null;
        String[] selectionArgs = null;
        String sortOrder = null;

        if (queryArgs != null) {
            selection = queryArgs.getString(ContentResolver.QUERY_ARG_SQL_SELECTION);
            selectionArgs = queryArgs.getStringArray(ContentResolver.QUERY_ARG_SQL_SELECTION_ARGS);
            sortOrder = queryArgs.getString(ContentResolver.QUERY_ARG_SQL_SORT_ORDER);
            if (sortOrder == null
                    && queryArgs.containsKey(ContentResolver.QUERY_ARG_SORT_COLUMNS)) {
                sortOrder = ContentResolver.createSqlSortClause(queryArgs);
            }
        }

        uri = safeUncanonicalize(uri);

        final String volumeName = getVolumeName(uri);
        final int targetSdkVersion = getCallingPackageTargetSdkVersion();
        final boolean allowHidden = isCallingPackageAllowedHidden();
        final int table = matchUri(uri, allowHidden);

        //Log.v(TAG, "query: uri="+uri+", selection="+selection);
        // handle MEDIA_SCANNER before calling getDatabaseForUri()
        if (table == MEDIA_SCANNER) {
            // create a cursor to return volume currently being scanned by the media scanner
            MatrixCursor c = new MatrixCursor(new String[] {MediaStore.MEDIA_SCANNER_VOLUME});
            c.addRow(new String[] {mMediaScannerVolume});
            return c;
        }

        // Used temporarily (until we have unique media IDs) to get an identifier
        // for the current sd card, so that the music app doesn't have to use the
        // non-public getFatVolumeId method
        if (table == FS_ID) {
            MatrixCursor c = new MatrixCursor(new String[] {"fsid"});
            c.addRow(new Integer[] {mVolumeId});
            return c;
        }

        if (table == VERSION) {
            MatrixCursor c = new MatrixCursor(new String[] {"version"});
            c.addRow(new Integer[] {getDatabaseVersion(getContext())});
            return c;
        }

        final DatabaseHelper helper;
        final SQLiteDatabase db;
        try {
            helper = getDatabaseForUri(uri);
            db = helper.getReadableDatabase();
        } catch (VolumeNotFoundException e) {
            return e.translateForQuery(targetSdkVersion);
        }

        if (table == MTP_OBJECT_REFERENCES) {
            final int handle = Integer.parseInt(uri.getPathSegments().get(2));
            return getObjectReferences(helper, db, handle);
        }

        SQLiteQueryBuilder qb = getQueryBuilder(TYPE_QUERY, uri, table, queryArgs);
        String limit = uri.getQueryParameter(MediaStore.PARAM_LIMIT);
        String filter = uri.getQueryParameter("filter");
        String [] keywords = null;
        if (filter != null) {
            filter = Uri.decode(filter).trim();
            if (!TextUtils.isEmpty(filter)) {
                String [] searchWords = filter.split(" ");
                keywords = new String[searchWords.length];
                for (int i = 0; i < searchWords.length; i++) {
                    String key = MediaStore.Audio.keyFor(searchWords[i]);
                    key = key.replace("\\", "\\\\");
                    key = key.replace("%", "\\%");
                    key = key.replace("_", "\\_");
                    keywords[i] = key;
                }
            }
        }

        String keywordColumn = null;
        switch (table) {
            case AUDIO_MEDIA:
            case AUDIO_GENRES_ALL_MEMBERS:
            case AUDIO_GENRES_ID_MEMBERS:
            case AUDIO_PLAYLISTS_ID_MEMBERS_ID:
            case AUDIO_PLAYLISTS_ID_MEMBERS:
                keywordColumn = MediaStore.Audio.Media.ARTIST_KEY +
                        "||" + MediaStore.Audio.Media.ALBUM_KEY +
                        "||" + MediaStore.Audio.Media.TITLE_KEY;
                break;
            case AUDIO_ARTISTS_ID_ALBUMS:
            case AUDIO_ALBUMS:
                keywordColumn = MediaStore.Audio.Media.ARTIST_KEY + "||"
                        + MediaStore.Audio.Media.ALBUM_KEY;
                break;
            case AUDIO_ARTISTS:
                keywordColumn = MediaStore.Audio.Media.ARTIST_KEY;
                break;
        }

        if (keywordColumn != null) {
            for (int i = 0; keywords != null && i < keywords.length; i++) {
                appendWhereStandalone(qb, keywordColumn + " LIKE ? ESCAPE '\\'",
                        "%" + keywords[i] + "%");
            }
        }

        String groupBy = null;
        if (table == AUDIO_ARTISTS_ID_ALBUMS) {
            groupBy = "audio.album_id";
        }

        if (getCallingPackageTargetSdkVersion() < Build.VERSION_CODES.Q) {
            // Some apps are abusing the "WHERE" clause by injecting "GROUP BY"
            // clauses; gracefully lift them out.
            final Pair<String, String> selectionAndGroupBy = recoverAbusiveGroupBy(
                    Pair.create(selection, groupBy));
            selection = selectionAndGroupBy.first;
            groupBy = selectionAndGroupBy.second;

            // Some apps are abusing the first column to inject "DISTINCT";
            // gracefully lift them out.
            if (!ArrayUtils.isEmpty(projection) && projection[0].startsWith("DISTINCT ")) {
                projection[0] = projection[0].substring("DISTINCT ".length());
                qb.setDistinct(true);
            }

            // Some apps are generating thumbnails with getThumbnail(), but then
            // ignoring the returned Bitmap and querying the raw table; give
            // them a row with enough information to find the original image.
            if ((table == IMAGES_THUMBNAILS || table == VIDEO_THUMBNAILS)
                    && !TextUtils.isEmpty(selection)) {
                final Matcher matcher = PATTERN_SELECTION_ID.matcher(selection);
                if (matcher.matches()) {
                    final long id = Long.parseLong(matcher.group(1));

                    final Uri fullUri;
                    if (table == IMAGES_THUMBNAILS) {
                        fullUri = ContentUris.withAppendedId(
                                Images.Media.getContentUri(volumeName), id);
                    } else if (table == VIDEO_THUMBNAILS) {
                        fullUri = ContentUris.withAppendedId(
                                Video.Media.getContentUri(volumeName), id);
                    } else {
                        throw new IllegalArgumentException();
                    }

                    final MatrixCursor cursor = new MatrixCursor(projection);
                    try {
                        String data = null;
                        if (ContentResolver.DEPRECATE_DATA_COLUMNS) {
                            // Go through provider to escape sandbox
                            data = ContentResolver.translateDeprecatedDataPath(
                                    fullUri.buildUpon().appendPath("thumbnail").build());
                        } else {
                            // Go directly to thumbnail file on disk
                            data = ensureThumbnail(fullUri, signal).getAbsolutePath();
                        }
                        cursor.newRow().add(MediaColumns._ID, null)
                                .add(Images.Thumbnails.IMAGE_ID, id)
                                .add(Video.Thumbnails.VIDEO_ID, id)
                                .add(MediaColumns.DATA, data);
                    } catch (FileNotFoundException ignored) {
                        // Return empty cursor if we had thumbnail trouble
                    }
                    return cursor;
                }
            }
        }

        final String having = null;
        final Cursor c = qb.query(db, projection,
                selection, selectionArgs, groupBy, having, sortOrder, limit, signal);

        if (c != null) {
            ((AbstractCursor) c).setNotificationUris(getContext().getContentResolver(),
                    Arrays.asList(uri), UserHandle.myUserId(), false);
        }

        return c;
    }

    @Override
    public String getType(Uri url) {
        final int match = matchUri(url, true);
        switch (match) {
            case IMAGES_MEDIA_ID:
            case AUDIO_MEDIA_ID:
            case AUDIO_PLAYLISTS_ID_MEMBERS_ID:
            case VIDEO_MEDIA_ID:
            case DOWNLOADS_ID:
            case FILES_ID:
                final LocalCallingIdentity token = clearLocalCallingIdentity();
                try (Cursor cursor = queryForSingleItem(url,
                        new String[] { MediaColumns.MIME_TYPE }, null, null, null)) {
                    return cursor.getString(0);
                } catch (FileNotFoundException e) {
                    throw new IllegalArgumentException(e.getMessage());
                } finally {
                     restoreLocalCallingIdentity(token);
                }

            case IMAGES_MEDIA:
            case IMAGES_THUMBNAILS:
                return Images.Media.CONTENT_TYPE;

            case AUDIO_ALBUMART_ID:
            case AUDIO_ALBUMART_FILE_ID:
            case IMAGES_THUMBNAILS_ID:
            case VIDEO_THUMBNAILS_ID:
                return "image/jpeg";

            case AUDIO_MEDIA:
            case AUDIO_GENRES_ID_MEMBERS:
            case AUDIO_PLAYLISTS_ID_MEMBERS:
                return Audio.Media.CONTENT_TYPE;

            case AUDIO_GENRES:
            case AUDIO_MEDIA_ID_GENRES:
                return Audio.Genres.CONTENT_TYPE;
            case AUDIO_GENRES_ID:
            case AUDIO_MEDIA_ID_GENRES_ID:
                return Audio.Genres.ENTRY_CONTENT_TYPE;
            case AUDIO_PLAYLISTS:
            case AUDIO_MEDIA_ID_PLAYLISTS:
                return Audio.Playlists.CONTENT_TYPE;
            case AUDIO_PLAYLISTS_ID:
            case AUDIO_MEDIA_ID_PLAYLISTS_ID:
                return Audio.Playlists.ENTRY_CONTENT_TYPE;

            case VIDEO_MEDIA:
                return Video.Media.CONTENT_TYPE;
            case DOWNLOADS:
                return Downloads.CONTENT_TYPE;
        }
        throw new IllegalStateException("Unknown URL : " + url);
    }

    @VisibleForTesting
    static void ensureFileColumns(Uri uri, ContentValues values) throws VolumeArgumentException {
        ensureNonUniqueFileColumns(matchUri(uri, true), uri, values, null /* currentPath */);
    }

    private static void ensureUniqueFileColumns(int match, Uri uri, ContentValues values)
            throws VolumeArgumentException {
        ensureFileColumns(match, uri, values, true, null /* currentPath */);
    }

    private static void ensureNonUniqueFileColumns(int match, Uri uri, ContentValues values,
            @Nullable String currentPath) throws VolumeArgumentException {
        ensureFileColumns(match, uri, values, false, currentPath);
    }

    /**
     * Get the various file-related {@link MediaColumns} in the given
     * {@link ContentValues} into sane condition. Also validates that defined
     * columns are valid for the given {@link Uri}, such as ensuring that only
     * {@code image/*} can be inserted into
     * {@link android.provider.MediaStore.Images}.
     */
    private static void ensureFileColumns(int match, Uri uri, ContentValues values,
            boolean makeUnique, @Nullable String currentPath) throws VolumeArgumentException {
        Trace.traceBegin(TRACE_TAG_DATABASE, "ensureFileColumns");

        // Figure out defaults based on Uri being modified
        String defaultMimeType = ContentResolver.MIME_TYPE_DEFAULT;
        String defaultPrimary = Environment.DIRECTORY_DOWNLOADS;
        String defaultSecondary = null;
        List<String> allowedPrimary = Arrays.asList(
                Environment.DIRECTORY_DOWNLOADS,
                Environment.DIRECTORY_DOCUMENTS);
        switch (match) {
            case AUDIO_MEDIA:
            case AUDIO_MEDIA_ID:
                defaultMimeType = "audio/mpeg";
                defaultPrimary = Environment.DIRECTORY_MUSIC;
                allowedPrimary = Arrays.asList(
                        Environment.DIRECTORY_ALARMS,
                        Environment.DIRECTORY_MUSIC,
                        Environment.DIRECTORY_NOTIFICATIONS,
                        Environment.DIRECTORY_PODCASTS,
                        Environment.DIRECTORY_RINGTONES);
                break;
            case VIDEO_MEDIA:
            case VIDEO_MEDIA_ID:
                defaultMimeType = "video/mp4";
                defaultPrimary = Environment.DIRECTORY_MOVIES;
                allowedPrimary = Arrays.asList(
                        Environment.DIRECTORY_DCIM,
                        Environment.DIRECTORY_MOVIES);
                break;
            case IMAGES_MEDIA:
            case IMAGES_MEDIA_ID:
                defaultMimeType = "image/jpeg";
                defaultPrimary = Environment.DIRECTORY_PICTURES;
                allowedPrimary = Arrays.asList(
                        Environment.DIRECTORY_DCIM,
                        Environment.DIRECTORY_PICTURES);
                break;
            case AUDIO_ALBUMART:
            case AUDIO_ALBUMART_ID:
                defaultMimeType = "image/jpeg";
                defaultPrimary = Environment.DIRECTORY_MUSIC;
                allowedPrimary = Arrays.asList(defaultPrimary);
                defaultSecondary = ".thumbnails";
                break;
            case VIDEO_THUMBNAILS:
            case VIDEO_THUMBNAILS_ID:
                defaultMimeType = "image/jpeg";
                defaultPrimary = Environment.DIRECTORY_MOVIES;
                allowedPrimary = Arrays.asList(defaultPrimary);
                defaultSecondary = ".thumbnails";
                break;
            case IMAGES_THUMBNAILS:
            case IMAGES_THUMBNAILS_ID:
                defaultMimeType = "image/jpeg";
                defaultPrimary = Environment.DIRECTORY_PICTURES;
                allowedPrimary = Arrays.asList(defaultPrimary);
                defaultSecondary = ".thumbnails";
                break;
            case AUDIO_PLAYLISTS:
            case AUDIO_PLAYLISTS_ID:
                defaultPrimary = Environment.DIRECTORY_MUSIC;
                allowedPrimary = Arrays.asList(defaultPrimary);
                break;
            case DOWNLOADS:
            case DOWNLOADS_ID:
                defaultPrimary = Environment.DIRECTORY_DOWNLOADS;
                allowedPrimary = Arrays.asList(defaultPrimary);
                break;
            case FILES:
            case FILES_ID:
                // Use defaults above
                break;
            default:
                Log.w(TAG, "Unhandled location " + uri + "; assuming generic files");
                break;
        }

        final String resolvedVolumeName = resolveVolumeName(uri);

        if (TextUtils.isEmpty(values.getAsString(MediaColumns.DATA))
                && MediaStore.VOLUME_INTERNAL.equals(resolvedVolumeName)) {
            // TODO: promote this to top-level check
            throw new UnsupportedOperationException(
                    "Writing to internal storage is not supported.");
        }

        // Force values when raw path provided
        if (!TextUtils.isEmpty(values.getAsString(MediaColumns.DATA))) {
            final String data = values.getAsString(MediaColumns.DATA);

            if (TextUtils.isEmpty(values.getAsString(MediaColumns.DISPLAY_NAME))) {
                values.put(MediaColumns.DISPLAY_NAME, extractDisplayName(data));
            }
            if (TextUtils.isEmpty(values.getAsString(MediaColumns.MIME_TYPE))) {
                values.put(MediaColumns.MIME_TYPE, MediaFile.getMimeTypeForFile(data));
            }
        }

        // Give ourselves sane defaults when missing
        if (TextUtils.isEmpty(values.getAsString(MediaColumns.DISPLAY_NAME))) {
            values.put(MediaColumns.DISPLAY_NAME,
                    String.valueOf(System.currentTimeMillis()));
        }
        final Integer formatObject = values.getAsInteger(FileColumns.FORMAT);
        final int format = formatObject == null ? 0 : formatObject.intValue();
        if (format == MtpConstants.FORMAT_ASSOCIATION) {
            values.putNull(MediaColumns.MIME_TYPE);
        } else if (TextUtils.isEmpty(values.getAsString(MediaColumns.MIME_TYPE))) {
            values.put(MediaColumns.MIME_TYPE, defaultMimeType);
        }

        // Sanity check MIME type against table
        final String mimeType = values.getAsString(MediaColumns.MIME_TYPE);
        if (mimeType != null && !defaultMimeType.equals(ContentResolver.MIME_TYPE_DEFAULT)) {
            final String[] split = defaultMimeType.split("/");
            if (!mimeType.startsWith(split[0])) {
                throw new IllegalArgumentException(
                        "MIME type " + mimeType + " cannot be inserted into " + uri
                                + "; expected MIME type under " + split[0] + "/*");
            }
        }

        // Generate path when undefined
        if (TextUtils.isEmpty(values.getAsString(MediaColumns.DATA))) {
            // Combine together deprecated columns when path undefined
            if (TextUtils.isEmpty(values.getAsString(MediaColumns.RELATIVE_PATH))) {
                String primary = values.getAsString(MediaColumns.PRIMARY_DIRECTORY);
                String secondary = values.getAsString(MediaColumns.SECONDARY_DIRECTORY);

                // Fall back to defaults when caller left undefined
                if (TextUtils.isEmpty(primary)) primary = defaultPrimary;
                if (TextUtils.isEmpty(secondary)) secondary = defaultSecondary;

                if (primary != null) {
                    if (secondary != null) {
                        values.put(MediaColumns.RELATIVE_PATH, primary + '/' + secondary + '/');
                    } else {
                        values.put(MediaColumns.RELATIVE_PATH, primary + '/');
                    }
                }
            }

            final String[] relativePath = sanitizePath(
                    values.getAsString(MediaColumns.RELATIVE_PATH));
            final String displayName = sanitizeDisplayName(
                    values.getAsString(MediaColumns.DISPLAY_NAME));

            // Create result file
            File res;
            try {
                res = getVolumePath(resolvedVolumeName);
            } catch (FileNotFoundException e) {
                throw new IllegalArgumentException(e);
            }
            res = Environment.buildPath(res, relativePath);
            try {
                if (makeUnique) {
                    res = FileUtils.buildUniqueFile(res, mimeType, displayName);
                } else {
                    res = FileUtils.buildNonUniqueFile(res, mimeType, displayName);
                }
            } catch (FileNotFoundException e) {
                throw new IllegalStateException(
                        "Failed to build unique file: " + res + " " + displayName + " " + mimeType);
            }

            // Check for shady looking paths

            // Require content live under specific directories, but allow in-place updates of
            // existing content that lives in the invalid directory.
            final String primary = relativePath[0];
            if (!res.getAbsolutePath().equals(currentPath) && !allowedPrimary.contains(primary)) {
                throw new IllegalArgumentException(
                        "Primary directory " + primary + " not allowed for " + uri
                                + "; allowed directories are " + allowedPrimary);
            }

            // Ensure all parent folders of result file exist
            res.getParentFile().mkdirs();
            if (!res.getParentFile().exists()) {
                throw new IllegalStateException("Failed to create directory: " + res);
            }
            values.put(MediaColumns.DATA, res.getAbsolutePath());
        } else {
            assertFileColumnsSane(match, uri, values);
        }

        // Drop columns that aren't relevant for special tables
        switch (match) {
            case AUDIO_ALBUMART:
            case VIDEO_THUMBNAILS:
            case IMAGES_THUMBNAILS:
            case AUDIO_PLAYLISTS:
                values.remove(MediaColumns.DISPLAY_NAME);
                values.remove(MediaColumns.MIME_TYPE);
                break;
        }

        Trace.traceEnd(TRACE_TAG_DATABASE);
    }

    private static @NonNull String[] sanitizePath(@Nullable String path) {
        if (path == null) {
            return EmptyArray.STRING;
        } else {
            final String[] segments = path.split("/");
            for (int i = 0; i < segments.length; i++) {
                segments[i] = sanitizeDisplayName(segments[i]);
            }
            return segments;
        }
    }

    private static @Nullable String sanitizeDisplayName(@Nullable String name) {
        if (name == null) {
            return null;
        } else if (name.startsWith(".")) {
            // The resulting file must not be hidden.
            return FileUtils.buildValidFatFilename("_" + name);
        } else {
            return FileUtils.buildValidFatFilename(name);
        }
    }

    /**
     * Sanity check that any requested {@link MediaColumns#DATA} paths actually
     * live on the storage volume being targeted.
     */
    private static void assertFileColumnsSane(int match, Uri uri, ContentValues values)
            throws VolumeArgumentException {
        if (!values.containsKey(MediaColumns.DATA)) return;
        try {
            // Sanity check that the requested path actually lives on volume
            final String volumeName = resolveVolumeName(uri);
            final Collection<File> allowed = getVolumeScanPaths(volumeName);
            final File actual = new File(values.getAsString(MediaColumns.DATA))
                    .getCanonicalFile();
            if (!FileUtils.contains(allowed, actual)) {
                throw new VolumeArgumentException(actual, allowed);
            }
        } catch (IOException e) {
            throw new IllegalArgumentException(e);
        }
    }

    @Override
    public int bulkInsert(Uri uri, ContentValues values[]) {
        final int targetSdkVersion = getCallingPackageTargetSdkVersion();
        final boolean allowHidden = isCallingPackageAllowedHidden();
        final int match = matchUri(uri, allowHidden);

        if (match == VOLUMES) {
            return super.bulkInsert(uri, values);
        }

        final DatabaseHelper helper;
        final SQLiteDatabase db;
        try {
            helper = getDatabaseForUri(uri);
            db = helper.getWritableDatabase();
        } catch (VolumeNotFoundException e) {
            return e.translateForUpdateDelete(targetSdkVersion);
        }

        if (match == MTP_OBJECT_REFERENCES) {
            int handle = Integer.parseInt(uri.getPathSegments().get(2));
            return setObjectReferences(helper, db, handle, values);
        }

        helper.beginTransaction();
        try {
            final int result = super.bulkInsert(uri, values);
            helper.setTransactionSuccessful();
            return result;
        } finally {
            helper.endTransaction();
        }
    }

    private int playlistBulkInsert(SQLiteDatabase db, Uri uri, ContentValues values[]) {
        DatabaseUtils.InsertHelper helper =
            new DatabaseUtils.InsertHelper(db, "audio_playlists_map");
        int audioidcolidx = helper.getColumnIndex(MediaStore.Audio.Playlists.Members.AUDIO_ID);
        int playlistididx = helper.getColumnIndex(Audio.Playlists.Members.PLAYLIST_ID);
        int playorderidx = helper.getColumnIndex(MediaStore.Audio.Playlists.Members.PLAY_ORDER);
        long playlistId = Long.parseLong(uri.getPathSegments().get(3));

        db.beginTransaction();
        int numInserted = 0;
        try {
            int len = values.length;
            for (int i = 0; i < len; i++) {
                helper.prepareForInsert();
                // getting the raw Object and converting it long ourselves saves
                // an allocation (the alternative is ContentValues.getAsLong, which
                // returns a Long object)
                long audioid = ((Number) values[i].get(
                        MediaStore.Audio.Playlists.Members.AUDIO_ID)).longValue();
                helper.bind(audioidcolidx, audioid);
                helper.bind(playlistididx, playlistId);
                // convert to int ourselves to save an allocation.
                int playorder = ((Number) values[i].get(
                        MediaStore.Audio.Playlists.Members.PLAY_ORDER)).intValue();
                helper.bind(playorderidx, playorder);
                helper.execute();
            }
            numInserted = len;
            db.setTransactionSuccessful();
        } finally {
            db.endTransaction();
            helper.close();
        }
        getContext().getContentResolver().notifyChange(uri, null);
        return numInserted;
    }

    private long insertDirectory(DatabaseHelper helper, SQLiteDatabase db, String path) {
        if (LOCAL_LOGV) Log.v(TAG, "inserting directory " + path);
        ContentValues values = new ContentValues();
        values.put(FileColumns.FORMAT, MtpConstants.FORMAT_ASSOCIATION);
        values.put(FileColumns.DATA, path);
        values.put(FileColumns.PARENT, getParent(helper, db, path));
        values.put(FileColumns.OWNER_PACKAGE_NAME, extractPathOwnerPackageName(path));
        values.put(FileColumns.VOLUME_NAME, extractVolumeName(path));
        values.put(FileColumns.RELATIVE_PATH, extractRelativePath(path));
        values.put(FileColumns.DISPLAY_NAME, extractDisplayName(path));
        values.put(FileColumns.IS_DOWNLOAD, isDownload(path));
        File file = new File(path);
        if (file.exists()) {
            values.put(FileColumns.DATE_MODIFIED, file.lastModified() / 1000);
        }
        long rowId = db.insert("files", FileColumns.DATE_MODIFIED, values);
        return rowId;
    }

    private static @Nullable String extractVolumeName(@Nullable String data) {
        if (data == null) return null;
        final Matcher matcher = PATTERN_VOLUME_NAME.matcher(data);
        if (matcher.find()) {
            final String volumeName = matcher.group(1);
            if (volumeName.equals("emulated")) {
                return MediaStore.VOLUME_EXTERNAL_PRIMARY;
            } else {
                return StorageVolume.normalizeUuid(volumeName);
            }
        } else {
            return MediaStore.VOLUME_INTERNAL;
        }
    }

    private static @Nullable String extractRelativePath(@Nullable String data) {
        if (data == null) return null;

        final String path;
        try {
            path = getCanonicalPath(data);
        } catch (IOException e) {
            Log.d(TAG, "Unable to get canonical path from invalid data path: " + data, e);
            return null;
        }

        final Matcher matcher = PATTERN_RELATIVE_PATH.matcher(path);
        if (matcher.find()) {
            final int lastSlash = path.lastIndexOf('/');
            if (lastSlash == -1 || lastSlash < matcher.end()) {
                // This is a file in the top-level directory, so relative path is "/"
                // which is different than null, which means unknown path
                return "/";
            } else {
                return path.substring(matcher.end(), lastSlash + 1);
            }
        } else {
            return null;
        }
    }

    private static @Nullable String extractDisplayName(@Nullable String data) {
        if (data == null) return null;
        if (data.endsWith("/")) {
            data = data.substring(0, data.length() - 1);
        }
        return data.substring(data.lastIndexOf('/') + 1);
    }

    private long getParent(DatabaseHelper helper, SQLiteDatabase db, String path) {
        final String parentPath = new File(path).getParent();
        if (Objects.equals("/", parentPath)) {
            return -1;
        } else {
            synchronized (mDirectoryCache) {
                Long id = mDirectoryCache.get(parentPath);
                if (id != null) {
                    return id;
                }
            }

            final long id;
            try (Cursor c = db.query("files", new String[] { FileColumns._ID },
                    FileColumns.DATA + "=?", new String[] { parentPath }, null, null, null)) {
                if (c.moveToFirst()) {
                    id = c.getLong(0);
                } else {
                    id = insertDirectory(helper, db, parentPath);
                }
            }

            synchronized (mDirectoryCache) {
                mDirectoryCache.put(parentPath, id);
            }
            return id;
        }
    }

    /**
     * @param c the Cursor whose title to retrieve
     * @return the result of {@link #getDefaultTitle(String)} if the result is valid; otherwise
     * the value of the {@code MediaStore.Audio.Media.TITLE} column
     */
    private String getDefaultTitleFromCursor(Cursor c) {
        String title = null;
        final int columnIndex = c.getColumnIndex("title_resource_uri");
        // Necessary to check for existence because we may be reading from an old DB version
        if (columnIndex > -1) {
            final String titleResourceUri = c.getString(columnIndex);
            if (titleResourceUri != null) {
                try {
                    title = getDefaultTitle(titleResourceUri);
                } catch (Exception e) {
                    // Best attempt only
                }
            }
        }
        if (title == null) {
            title = c.getString(c.getColumnIndex(MediaStore.Audio.Media.TITLE));
        }
        return title;
    }

    /**
     * @param title_resource_uri The title resource for which to retrieve the default localization
     * @return The title localized to {@code Locale.US}, or {@code null} if unlocalizable
     * @throws Exception Thrown if the title appears to be localizable, but the localization failed
     * for any reason. For example, the application from which the localized title is fetched is not
     * installed, or it does not have the resource which needs to be localized
     */
    private String getDefaultTitle(String title_resource_uri) throws Exception{
        try {
            return getTitleFromResourceUri(title_resource_uri, false);
        } catch (Exception e) {
            Log.e(TAG, "Error getting default title for " + title_resource_uri, e);
            throw e;
        }
    }

    /**
     * @param title_resource_uri The title resource to localize
     * @return The localized title, or {@code null} if unlocalizable
     * @throws Exception Thrown if the title appears to be localizable, but the localization failed
     * for any reason. For example, the application from which the localized title is fetched is not
     * installed, or it does not have the resource which needs to be localized
     */
    private String getLocalizedTitle(String title_resource_uri) throws Exception {
        try {
            return getTitleFromResourceUri(title_resource_uri, true);
        } catch (Exception e) {
            Log.e(TAG, "Error getting localized title for " + title_resource_uri, e);
            throw e;
        }
    }

    /**
     * Localizable titles conform to this URI pattern:
     *   Scheme: {@link ContentResolver.SCHEME_ANDROID_RESOURCE}
     *   Authority: Package Name of ringtone title provider
     *   First Path Segment: Type of resource (must be "string")
     *   Second Path Segment: Resource name of title
     *
     * @param title_resource_uri The title resource to retrieve
     * @param localize Whether or not to localize the title
     * @return The title, or {@code null} if unlocalizable
     * @throws Exception Thrown if the title appears to be localizable, but the localization failed
     * for any reason. For example, the application from which the localized title is fetched is not
     * installed, or it does not have the resource which needs to be localized
     */
    private String getTitleFromResourceUri(String title_resource_uri, boolean localize)
        throws Exception {
        if (TextUtils.isEmpty(title_resource_uri)) {
            return null;
        }
        final Uri titleUri = Uri.parse(title_resource_uri);
        final String scheme = titleUri.getScheme();
        if (!ContentResolver.SCHEME_ANDROID_RESOURCE.equals(scheme)) {
            return null;
        }
        final List<String> pathSegments = titleUri.getPathSegments();
        if (pathSegments.size() != 2) {
            Log.e(TAG, "Error getting localized title for " + title_resource_uri
                + ", must have 2 path segments");
            return null;
        }
        final String type = pathSegments.get(0);
        if (!"string".equals(type)) {
            Log.e(TAG, "Error getting localized title for " + title_resource_uri
                + ", first path segment must be \"string\"");
            return null;
        }
        final String packageName = titleUri.getAuthority();
        final Resources resources;
        if (localize) {
            resources = mPackageManager.getResourcesForApplication(packageName);
        } else {
            final Context packageContext = getContext().createPackageContext(packageName, 0);
            final Configuration configuration = packageContext.getResources().getConfiguration();
            configuration.setLocale(Locale.US);
            resources = packageContext.createConfigurationContext(configuration).getResources();
        }
        final String resourceIdentifier = pathSegments.get(1);
        final int id = resources.getIdentifier(resourceIdentifier, type, packageName);
        return resources.getString(id);
    }

    public void onLocaleChanged() {
        localizeTitles();
    }

    private void localizeTitles() {
        final DatabaseHelper helper = mInternalDatabase;
        final SQLiteDatabase db = helper.getWritableDatabase();

        try (Cursor c = db.query("files", new String[]{"_id", "title_resource_uri"},
            "title_resource_uri IS NOT NULL", null, null, null, null)) {
            while (c.moveToNext()) {
                final String id = c.getString(0);
                final String titleResourceUri = c.getString(1);
                final ContentValues values = new ContentValues();
                try {
                    final String localizedTitle = getLocalizedTitle(titleResourceUri);
                    values.put("title_key", MediaStore.Audio.keyFor(localizedTitle));
                    // do a final trim of the title, in case it started with the special
                    // "sort first" character (ascii \001)
                    values.put("title", localizedTitle.trim());
                    db.update("files", values, "_id=?", new String[]{id});
                } catch (Exception e) {
                    Log.e(TAG, "Error updating localized title for " + titleResourceUri
                        + ", keeping old localization");
                }
            }
        }
    }

    private long insertFile(DatabaseHelper helper, int match, Uri uri, ContentValues values,
            int mediaType, boolean notify) {
        final SQLiteDatabase db = helper.getWritableDatabase();

        boolean wasPathEmpty = !values.containsKey(MediaStore.MediaColumns.DATA)
                || TextUtils.isEmpty(values.getAsString(MediaStore.MediaColumns.DATA));

        // Make sure all file-related columns are defined
        try {
            ensureUniqueFileColumns(match, uri, values);
        } catch (VolumeArgumentException e) {
            if (getCallingPackageTargetSdkVersion() >= Build.VERSION_CODES.Q) {
                throw new IllegalArgumentException(e.getMessage());
            } else {
                Log.w(TAG, e.getMessage());
                return 0;
            }
        }

        switch (mediaType) {
            case FileColumns.MEDIA_TYPE_IMAGE: {
                values.put(MediaStore.MediaColumns.DATE_ADDED, System.currentTimeMillis() / 1000);
                break;
            }

            case FileColumns.MEDIA_TYPE_AUDIO: {
                // SQLite Views are read-only, so we need to deconstruct this
                // insert and do inserts into the underlying tables.
                // If doing this here turns out to be a performance bottleneck,
                // consider moving this to native code and using triggers on
                // the view.
                String albumartist = values.getAsString(MediaStore.Audio.Media.ALBUM_ARTIST);
                String compilation = values.getAsString(MediaStore.Audio.Media.COMPILATION);
                values.remove(MediaStore.Audio.Media.COMPILATION);

                // Insert the artist into the artist table and remove it from
                // the input values
                Object so = values.get("artist");
                String s = (so == null ? "" : so.toString());
                values.remove("artist");
                long artistRowId;
                ArrayMap<String, Long> artistCache = helper.mArtistCache;
                String path = values.getAsString(MediaStore.MediaColumns.DATA);
                synchronized(artistCache) {
                    Long temp = artistCache.get(s);
                    if (temp == null) {
                        artistRowId = getKeyIdForName(helper, db,
                                "artists", "artist_key", "artist",
                                s, s, path, 0, null, artistCache, uri);
                    } else {
                        artistRowId = temp.longValue();
                    }
                }
                String artist = s;

                // Do the same for the album field
                so = values.get("album");
                s = (so == null ? "" : so.toString());
                values.remove("album");
                long albumRowId;
                ArrayMap<String, Long> albumCache = helper.mAlbumCache;
                synchronized(albumCache) {
                    int albumhash = 0;
                    if (albumartist != null) {
                        albumhash = albumartist.hashCode();
                    } else if (compilation != null && compilation.equals("1")) {
                        // nothing to do, hash already set
                    } else {
                        albumhash = path.substring(0, path.lastIndexOf('/')).hashCode();
                    }
                    String cacheName = s + albumhash;
                    Long temp = albumCache.get(cacheName);
                    if (temp == null) {
                        albumRowId = getKeyIdForName(helper, db,
                                "albums", "album_key", "album",
                                s, cacheName, path, albumhash, artist, albumCache, uri);
                    } else {
                        albumRowId = temp;
                    }
                }

                values.put("artist_id", Integer.toString((int)artistRowId));
                values.put("album_id", Integer.toString((int)albumRowId));
                so = values.getAsString("title");
                s = (so == null ? "" : so.toString());

                try {
                    final String localizedTitle = getLocalizedTitle(s);
                    if (localizedTitle != null) {
                        values.put("title_resource_uri", s);
                        s = localizedTitle;
                    } else {
                        values.putNull("title_resource_uri");
                    }
                } catch (Exception e) {
                    values.put("title_resource_uri", s);
                }
                values.put("title_key", MediaStore.Audio.keyFor(s));
                // do a final trim of the title, in case it started with the special
                // "sort first" character (ascii \001)
                values.put("title", s.trim());
                break;
            }

            case FileColumns.MEDIA_TYPE_VIDEO: {
                break;
            }
        }

        // compute bucket_id and bucket_display_name for all files
        String path = values.getAsString(MediaStore.MediaColumns.DATA);
        computeDataValues(values);
        values.put(MediaStore.MediaColumns.DATE_ADDED, System.currentTimeMillis() / 1000);

        long rowId = 0;
        Integer i = values.getAsInteger(
                MediaStore.MediaColumns.MEDIA_SCANNER_NEW_OBJECT_ID);
        if (i != null) {
            rowId = i.intValue();
            values = new ContentValues(values);
            values.remove(MediaStore.MediaColumns.MEDIA_SCANNER_NEW_OBJECT_ID);
        }

        String title = values.getAsString(MediaStore.MediaColumns.TITLE);
        if (title == null && path != null) {
            title = MediaFile.getFileTitle(path);
        }
        values.put(FileColumns.TITLE, title);

        String mimeType = null;
        int format = MtpConstants.FORMAT_ASSOCIATION;
        if (path != null && new File(path).isDirectory()) {
            values.put(FileColumns.FORMAT, MtpConstants.FORMAT_ASSOCIATION);
            values.putNull(MediaStore.MediaColumns.MIME_TYPE);
        } else {
            mimeType = values.getAsString(MediaStore.MediaColumns.MIME_TYPE);
            final Integer formatObject = values.getAsInteger(FileColumns.FORMAT);
            format = (formatObject == null ? 0 : formatObject.intValue());
        }

        if (format == 0) {
            if (TextUtils.isEmpty(path) || wasPathEmpty) {
                // special case device created playlists
                if (mediaType == FileColumns.MEDIA_TYPE_PLAYLIST) {
                    values.put(FileColumns.FORMAT, MtpConstants.FORMAT_ABSTRACT_AV_PLAYLIST);
                    // create a file path for the benefit of MTP
                    path = Environment.getExternalStorageDirectory()
                            + "/Playlists/" + values.getAsString(Audio.Playlists.NAME);
                    values.put(MediaStore.MediaColumns.DATA, path);
                    values.put(FileColumns.PARENT, 0);
                }
            } else {
                format = MediaFile.getFormatCode(path, mimeType);
            }
        }
        if (path != null && path.endsWith("/")) {
            Log.e(TAG, "directory has trailing slash: " + path);
            return 0;
        }
        if (format != 0) {
            values.put(FileColumns.FORMAT, format);
            if (mimeType == null && format != MtpConstants.FORMAT_ASSOCIATION) {
                mimeType = MediaFile.getMimeTypeForFormatCode(format);
            }
        }

        if (mimeType == null && path != null && format != MtpConstants.FORMAT_ASSOCIATION) {
            mimeType = MediaFile.getMimeTypeForFile(path);
        }

        if (mimeType != null) {
            values.put(FileColumns.MIME_TYPE, mimeType);

            // If 'values' contained the media type, then the caller wants us
            // to use that exact type, so don't override it based on mimetype
            if (!values.containsKey(FileColumns.MEDIA_TYPE) &&
                    mediaType == FileColumns.MEDIA_TYPE_NONE &&
                    !android.media.MediaScanner.isNoMediaPath(path)) {
                if (MediaFile.isAudioMimeType(mimeType)) {
                    mediaType = FileColumns.MEDIA_TYPE_AUDIO;
                } else if (MediaFile.isVideoMimeType(mimeType)) {
                    mediaType = FileColumns.MEDIA_TYPE_VIDEO;
                } else if (MediaFile.isImageMimeType(mimeType)) {
                    mediaType = FileColumns.MEDIA_TYPE_IMAGE;
                } else if (MediaFile.isPlayListMimeType(mimeType)) {
                    mediaType = FileColumns.MEDIA_TYPE_PLAYLIST;
                }
            }
        }
        values.put(FileColumns.MEDIA_TYPE, mediaType);

        if (rowId == 0) {
            if (mediaType == FileColumns.MEDIA_TYPE_PLAYLIST) {
                String name = values.getAsString(Audio.Playlists.NAME);
                if (name == null && path == null) {
                    // MediaScanner will compute the name from the path if we have one
                    throw new IllegalArgumentException(
                            "no name was provided when inserting abstract playlist");
                }
            } else {
                if (path == null) {
                    // path might be null for playlists created on the device
                    // or transfered via MTP
                    throw new IllegalArgumentException(
                            "no path was provided when inserting new file");
                }
            }

            // make sure modification date and size are set
            if (path != null) {
                File file = new File(path);
                if (file.exists()) {
                    values.put(FileColumns.DATE_MODIFIED, file.lastModified() / 1000);
                    if (!values.containsKey(FileColumns.SIZE)) {
                        values.put(FileColumns.SIZE, file.length());
                    }
                }
            }

            Long parent = values.getAsLong(FileColumns.PARENT);
            if (parent == null) {
                if (path != null) {
                    long parentId = getParent(helper, db, path);
                    values.put(FileColumns.PARENT, parentId);
                }
            }

            rowId = db.insert("files", FileColumns.DATE_MODIFIED, values);
        } else {
            db.update("files", values, FileColumns._ID + "=?",
                    new String[] { Long.toString(rowId) });
        }
        if (format == MtpConstants.FORMAT_ASSOCIATION) {
            synchronized (mDirectoryCache) {
                mDirectoryCache.put(path, rowId);
            }
        }

        return rowId;
    }

    private Cursor getObjectReferences(DatabaseHelper helper, SQLiteDatabase db, int handle) {
        Cursor c = db.query("files", sMediaTableColumns, "_id=?",
                new String[] {  Integer.toString(handle) },
                null, null, null);
        try {
            if (c != null && c.moveToNext()) {
                long playlistId = c.getLong(0);
                int mediaType = c.getInt(1);
                if (mediaType != FileColumns.MEDIA_TYPE_PLAYLIST) {
                    // we only support object references for playlist objects
                    return null;
                }
                return db.rawQuery(OBJECT_REFERENCES_QUERY,
                        new String[] { Long.toString(playlistId) } );
            }
        } finally {
            IoUtils.closeQuietly(c);
        }
        return null;
    }

    private int setObjectReferences(DatabaseHelper helper, SQLiteDatabase db,
            int handle, ContentValues values[]) {
        // first look up the media table and media ID for the object
        long playlistId = 0;
        Cursor c = db.query("files", sMediaTableColumns, "_id=?",
                new String[] {  Integer.toString(handle) },
                null, null, null);
        try {
            if (c != null && c.moveToNext()) {
                int mediaType = c.getInt(1);
                if (mediaType != FileColumns.MEDIA_TYPE_PLAYLIST) {
                    // we only support object references for playlist objects
                    return 0;
                }
                playlistId = c.getLong(0);
            }
        } finally {
            IoUtils.closeQuietly(c);
        }
        if (playlistId == 0) {
            return 0;
        }

        // next delete any existing entries
        db.delete("audio_playlists_map", "playlist_id=?",
                new String[] { Long.toString(playlistId) });

        // finally add the new entries
        int count = values.length;
        int added = 0;
        ContentValues[] valuesList = new ContentValues[count];
        for (int i = 0; i < count; i++) {
            // convert object ID to audio ID
            long audioId = 0;
            long objectId = values[i].getAsLong(MediaStore.MediaColumns._ID);
            c = db.query("files", sMediaTableColumns, "_id=?",
                    new String[] {  Long.toString(objectId) },
                    null, null, null);
            try {
                if (c != null && c.moveToNext()) {
                    int mediaType = c.getInt(1);
                    if (mediaType != FileColumns.MEDIA_TYPE_AUDIO) {
                        // we only allow audio files in playlists, so skip
                        continue;
                    }
                    audioId = c.getLong(0);
                }
            } finally {
                IoUtils.closeQuietly(c);
            }
            if (audioId != 0) {
                ContentValues v = new ContentValues();
                v.put(MediaStore.Audio.Playlists.Members.PLAYLIST_ID, playlistId);
                v.put(MediaStore.Audio.Playlists.Members.AUDIO_ID, audioId);
                v.put(MediaStore.Audio.Playlists.Members.PLAY_ORDER, added);
                valuesList[added++] = v;
            }
        }
        if (added < count) {
            // we weren't able to find everything on the list, so lets resize the array
            // and pass what we have.
            ContentValues[] newValues = new ContentValues[added];
            System.arraycopy(valuesList, 0, newValues, 0, added);
            valuesList = newValues;
        }

        int rowsChanged = playlistBulkInsert(db,
                Audio.Playlists.Members.getContentUri(MediaStore.VOLUME_EXTERNAL, playlistId),
                valuesList);

        if (rowsChanged > 0) {
            updatePlaylistDateModifiedToNow(db, playlistId);
        }

        return rowsChanged;
    }

    private static final String[] GENRE_LOOKUP_PROJECTION = new String[] {
            Audio.Genres._ID, // 0
            Audio.Genres.NAME, // 1
    };

    private void updateGenre(long rowId, String genre, String volumeName) {
        Uri uri = null;
        Cursor cursor = null;
        Uri genresUri = MediaStore.Audio.Genres.getContentUri(volumeName);
        try {
            // see if the genre already exists
            cursor = query(genresUri, GENRE_LOOKUP_PROJECTION, MediaStore.Audio.Genres.NAME + "=?",
                            new String[] { genre }, null);
            if (cursor == null || cursor.getCount() == 0) {
                // genre does not exist, so create the genre in the genre table
                ContentValues values = new ContentValues();
                values.put(MediaStore.Audio.Genres.NAME, genre);
                uri = insert(genresUri, values);
            } else {
                // genre already exists, so compute its Uri
                cursor.moveToNext();
                uri = ContentUris.withAppendedId(genresUri, cursor.getLong(0));
            }
            if (uri != null) {
                uri = Uri.withAppendedPath(uri, MediaStore.Audio.Genres.Members.CONTENT_DIRECTORY);
            }
        } finally {
            IoUtils.closeQuietly(cursor);
        }

        if (uri != null) {
            // add entry to audio_genre_map
            ContentValues values = new ContentValues();
            values.put(MediaStore.Audio.Genres.Members.AUDIO_ID, Long.valueOf(rowId));
            insert(uri, values);
        }
    }

    @VisibleForTesting
    static @Nullable String extractPathOwnerPackageName(@Nullable String path) {
        if (path == null) return null;
        final Matcher m = PATTERN_OWNED_PATH.matcher(path);
        if (m.matches()) {
            return m.group(1);
        } else {
            return null;
        }
    }

    private void maybePut(@NonNull ContentValues values, @NonNull String key,
            @Nullable String value) {
        if (value != null) {
            values.put(key, value);
        }
    }

    private boolean maybeMarkAsDownload(@NonNull ContentValues values) {
        final String path = values.getAsString(MediaColumns.DATA);
        if (path != null && isDownload(path)) {
            values.put(FileColumns.IS_DOWNLOAD, true);
            return true;
        }
        return false;
    }

    private static @NonNull String resolveVolumeName(@NonNull Uri uri) {
        final String volumeName = getVolumeName(uri);
        if (MediaStore.VOLUME_EXTERNAL.equals(volumeName)) {
            return MediaStore.VOLUME_EXTERNAL_PRIMARY;
        } else {
            return volumeName;
        }
    }

    @Override
    public Uri insert(Uri uri, ContentValues initialValues) {
        Trace.traceBegin(TRACE_TAG_DATABASE, "insert");
        try {
            return insertInternal(uri, initialValues);
        } finally {
            Trace.traceEnd(TRACE_TAG_DATABASE);
        }
    }

    private Uri insertInternal(Uri uri, ContentValues initialValues) {
        final boolean allowHidden = isCallingPackageAllowedHidden();
        final int match = matchUri(uri, allowHidden);

        final int targetSdkVersion = getCallingPackageTargetSdkVersion();
        final String originalVolumeName = getVolumeName(uri);
        final String resolvedVolumeName = resolveVolumeName(uri);

        // handle MEDIA_SCANNER before calling getDatabaseForUri()
        if (match == MEDIA_SCANNER) {
            mMediaScannerVolume = initialValues.getAsString(MediaStore.MEDIA_SCANNER_VOLUME);

            final DatabaseHelper helper;
            try {
                helper = getDatabaseForUri(MediaStore.Files.getContentUri(mMediaScannerVolume));
            } catch (VolumeNotFoundException e) {
                return e.translateForInsert(targetSdkVersion);
            }

            helper.mScanStartTime = SystemClock.currentTimeMicro();
            return MediaStore.getMediaScannerUri();
        }

        if (match == VOLUMES) {
            String name = initialValues.getAsString("name");
            Uri attachedVolume = attachVolume(name);
            if (mMediaScannerVolume != null && mMediaScannerVolume.equals(name)) {
                final DatabaseHelper helper;
                try {
                    helper = getDatabaseForUri(
                            MediaStore.Files.getContentUri(mMediaScannerVolume));
                } catch (VolumeNotFoundException e) {
                    return e.translateForInsert(targetSdkVersion);
                }
                helper.mScanStartTime = SystemClock.currentTimeMicro();
            }
            return attachedVolume;
        }

        String genre = null;
        String path = null;
        String ownerPackageName = null;
        if (initialValues != null) {
            // Ignore or augment incoming raw filesystem paths
            for (String column : sDataColumns.keySet()) {
                if (!initialValues.containsKey(column)) continue;

                if (isCallingPackageSystem() || isCallingPackageLegacy()) {
                    // Mutation allowed
                } else {
                    Log.w(TAG, "Ignoring mutation of  " + column + " from "
                            + getCallingPackageOrSelf());
                    initialValues.remove(column);
                }
            }

            genre = initialValues.getAsString(Audio.AudioColumns.GENRE);
            initialValues.remove(Audio.AudioColumns.GENRE);
            path = initialValues.getAsString(MediaStore.MediaColumns.DATA);

            if (!isCallingPackageSystem()) {
                initialValues.remove(FileColumns.IS_DOWNLOAD);
            }

            // We no longer track location metadata
            if (initialValues.containsKey(ImageColumns.LATITUDE)) {
                initialValues.putNull(ImageColumns.LATITUDE);
            }
            if (initialValues.containsKey(ImageColumns.LONGITUDE)) {
                initialValues.putNull(ImageColumns.LONGITUDE);
            }

            if (isCallingPackageSystem()) {
                // When media inserted by ourselves, the best we can do is guess
                // ownership based on path.
                ownerPackageName = initialValues.getAsString(FileColumns.OWNER_PACKAGE_NAME);
                if (TextUtils.isEmpty(ownerPackageName)) {
                    ownerPackageName = extractPathOwnerPackageName(path);
                }
            } else {
                // Remote callers have no direct control over owner column; we force
                // it be whoever is creating the content.
                initialValues.remove(FileColumns.OWNER_PACKAGE_NAME);
                ownerPackageName = getCallingPackageOrSelf();
            }
        }

        long rowId = -1;
        Uri newUri = null;

        final DatabaseHelper helper;
        final SQLiteDatabase db;
        try {
            helper = getDatabaseForUri(uri);
            db = helper.getWritableDatabase();
        } catch (VolumeNotFoundException e) {
            return e.translateForInsert(targetSdkVersion);
        }

        switch (match) {
            case IMAGES_MEDIA: {
                maybePut(initialValues, FileColumns.OWNER_PACKAGE_NAME, ownerPackageName);
                final boolean isDownload = maybeMarkAsDownload(initialValues);
                rowId = insertFile(helper, match, uri, initialValues,
                        FileColumns.MEDIA_TYPE_IMAGE, true);
                if (rowId > 0) {
                    MediaDocumentsProvider.onMediaStoreInsert(
                            getContext(), resolvedVolumeName, FileColumns.MEDIA_TYPE_IMAGE, rowId);
                    newUri = ContentUris.withAppendedId(
                            Images.Media.getContentUri(originalVolumeName), rowId);
                }
                break;
            }

            case IMAGES_THUMBNAILS: {
                if (helper.mInternal) {
                    throw new UnsupportedOperationException(
                            "Writing to internal storage is not supported.");
                }

                // Require that caller has write access to underlying media
                final long imageId = initialValues.getAsLong(MediaStore.Images.Thumbnails.IMAGE_ID);
                enforceCallingPermission(ContentUris.withAppendedId(
                        MediaStore.Images.Media.getContentUri(resolvedVolumeName), imageId), true);

                try {
                    ensureUniqueFileColumns(match, uri, initialValues);
                } catch (VolumeArgumentException e) {
                    return e.translateForInsert(targetSdkVersion);
                }

                rowId = db.insert("thumbnails", "name", initialValues);
                if (rowId > 0) {
                    newUri = ContentUris.withAppendedId(Images.Thumbnails.
                            getContentUri(originalVolumeName), rowId);
                }
                break;
            }

            case VIDEO_THUMBNAILS: {
                if (helper.mInternal) {
                    throw new UnsupportedOperationException(
                            "Writing to internal storage is not supported.");
                }

                // Require that caller has write access to underlying media
                final long videoId = initialValues.getAsLong(MediaStore.Video.Thumbnails.VIDEO_ID);
                enforceCallingPermission(ContentUris.withAppendedId(
                        MediaStore.Video.Media.getContentUri(resolvedVolumeName), videoId), true);

                try {
                    ensureUniqueFileColumns(match, uri, initialValues);
                } catch (VolumeArgumentException e) {
                    return e.translateForInsert(targetSdkVersion);
                }

                rowId = db.insert("videothumbnails", "name", initialValues);
                if (rowId > 0) {
                    newUri = ContentUris.withAppendedId(Video.Thumbnails.
                            getContentUri(originalVolumeName), rowId);
                }
                break;
            }

            case AUDIO_MEDIA: {
                maybePut(initialValues, FileColumns.OWNER_PACKAGE_NAME, ownerPackageName);
                final boolean isDownload = maybeMarkAsDownload(initialValues);
                rowId = insertFile(helper, match, uri, initialValues,
                        FileColumns.MEDIA_TYPE_AUDIO, true);
                if (rowId > 0) {
                    MediaDocumentsProvider.onMediaStoreInsert(
                            getContext(), resolvedVolumeName, FileColumns.MEDIA_TYPE_AUDIO, rowId);
                    newUri = ContentUris.withAppendedId(
                            Audio.Media.getContentUri(originalVolumeName), rowId);
                    if (genre != null) {
                        updateGenre(rowId, genre, resolvedVolumeName);
                    }
                }
                break;
            }

            case AUDIO_MEDIA_ID_GENRES: {
                // Require that caller has write access to underlying media
                final long audioId = Long.parseLong(uri.getPathSegments().get(2));
                enforceCallingPermission(ContentUris.withAppendedId(
                        MediaStore.Audio.Media.getContentUri(resolvedVolumeName), audioId), true);

                ContentValues values = new ContentValues(initialValues);
                values.put(Audio.Genres.Members.AUDIO_ID, audioId);
                rowId = db.insert("audio_genres_map", "genre_id", values);
                if (rowId > 0) {
                    newUri = ContentUris.withAppendedId(uri, rowId);
                }
                break;
            }

            case AUDIO_MEDIA_ID_PLAYLISTS: {
                // Require that caller has write access to underlying media
                final long audioId = Long.parseLong(uri.getPathSegments().get(2));
                enforceCallingPermission(ContentUris.withAppendedId(
                        MediaStore.Audio.Media.getContentUri(resolvedVolumeName), audioId), true);
                final long playlistId = initialValues
                        .getAsLong(MediaStore.Audio.Playlists.Members.PLAYLIST_ID);
                enforceCallingPermission(ContentUris.withAppendedId(
                        MediaStore.Audio.Playlists.getContentUri(resolvedVolumeName), playlistId), true);

                ContentValues values = new ContentValues(initialValues);
                values.put(Audio.Playlists.Members.AUDIO_ID, audioId);
                rowId = db.insert("audio_playlists_map", "playlist_id",
                        values);
                if (rowId > 0) {
                    newUri = ContentUris.withAppendedId(uri, rowId);
                    updatePlaylistDateModifiedToNow(db, playlistId);
                }
                break;
            }

            case AUDIO_GENRES: {
                // NOTE: No permission enforcement on genres
                rowId = db.insert("audio_genres", "audio_id", initialValues);
                if (rowId > 0) {
                    newUri = ContentUris.withAppendedId(
                            Audio.Genres.getContentUri(originalVolumeName), rowId);
                }
                break;
            }

            case AUDIO_GENRES_ID_MEMBERS: {
                // Require that caller has write access to underlying media
                final long audioId = initialValues
                        .getAsLong(MediaStore.Audio.Genres.Members.AUDIO_ID);
                enforceCallingPermission(ContentUris.withAppendedId(
                        MediaStore.Audio.Media.getContentUri(resolvedVolumeName), audioId), true);

                Long genreId = Long.parseLong(uri.getPathSegments().get(3));
                ContentValues values = new ContentValues(initialValues);
                values.put(Audio.Genres.Members.GENRE_ID, genreId);
                rowId = db.insert("audio_genres_map", "genre_id", values);
                if (rowId > 0) {
                    newUri = ContentUris.withAppendedId(uri, rowId);
                }
                break;
            }

            case AUDIO_PLAYLISTS: {
                maybePut(initialValues, FileColumns.OWNER_PACKAGE_NAME, ownerPackageName);
                final boolean isDownload = maybeMarkAsDownload(initialValues);
                ContentValues values = new ContentValues(initialValues);
                values.put(MediaStore.Audio.Playlists.DATE_ADDED, System.currentTimeMillis() / 1000);
                rowId = insertFile(helper, match, uri, values,
                        FileColumns.MEDIA_TYPE_PLAYLIST, true);
                if (rowId > 0) {
                    newUri = ContentUris.withAppendedId(
                            Audio.Playlists.getContentUri(originalVolumeName), rowId);
                }
                break;
            }

            case AUDIO_PLAYLISTS_ID:
            case AUDIO_PLAYLISTS_ID_MEMBERS: {
                // Require that caller has write access to underlying media
                final long audioId = initialValues
                        .getAsLong(MediaStore.Audio.Playlists.Members.AUDIO_ID);
                enforceCallingPermission(ContentUris.withAppendedId(
                        MediaStore.Audio.Media.getContentUri(resolvedVolumeName), audioId), true);
                final long playlistId = Long.parseLong(uri.getPathSegments().get(3));
                enforceCallingPermission(ContentUris.withAppendedId(
                        MediaStore.Audio.Playlists.getContentUri(resolvedVolumeName), playlistId), true);

                ContentValues values = new ContentValues(initialValues);
                values.put(Audio.Playlists.Members.PLAYLIST_ID, playlistId);
                rowId = db.insert("audio_playlists_map", "playlist_id", values);
                if (rowId > 0) {
                    newUri = ContentUris.withAppendedId(uri, rowId);
                    updatePlaylistDateModifiedToNow(db, playlistId);
                }
                break;
            }

            case VIDEO_MEDIA: {
                maybePut(initialValues, FileColumns.OWNER_PACKAGE_NAME, ownerPackageName);
                final boolean isDownload = maybeMarkAsDownload(initialValues);
                rowId = insertFile(helper, match, uri, initialValues,
                        FileColumns.MEDIA_TYPE_VIDEO, true);
                if (rowId > 0) {
                    MediaDocumentsProvider.onMediaStoreInsert(
                            getContext(), resolvedVolumeName, FileColumns.MEDIA_TYPE_VIDEO, rowId);
                    newUri = ContentUris.withAppendedId(
                            Video.Media.getContentUri(originalVolumeName), rowId);
                }
                break;
            }

            case AUDIO_ALBUMART: {
                if (helper.mInternal) {
                    throw new UnsupportedOperationException("no internal album art allowed");
                }

                try {
                    ensureUniqueFileColumns(match, uri, initialValues);
                } catch (VolumeArgumentException e) {
                    return e.translateForInsert(targetSdkVersion);
                }

                rowId = db.insert("album_art", MediaStore.MediaColumns.DATA, initialValues);
                if (rowId > 0) {
                    newUri = ContentUris.withAppendedId(uri, rowId);
                }
                break;
            }

            case FILES: {
                maybePut(initialValues, FileColumns.OWNER_PACKAGE_NAME, ownerPackageName);
                final boolean isDownload = maybeMarkAsDownload(initialValues);
                rowId = insertFile(helper, match, uri, initialValues,
                        FileColumns.MEDIA_TYPE_NONE, true);
                if (rowId > 0) {
                    MediaDocumentsProvider.onMediaStoreInsert(
                            getContext(), resolvedVolumeName, FileColumns.MEDIA_TYPE_NONE, rowId);
                    newUri = Files.getContentUri(originalVolumeName, rowId);
                }
                break;
            }

            case MTP_OBJECTS:
                // We don't send a notification if the insert originated from MTP
                final boolean isDownload = maybeMarkAsDownload(initialValues);
                rowId = insertFile(helper, match, uri, initialValues,
                        FileColumns.MEDIA_TYPE_NONE, false);
                if (rowId > 0) {
                    newUri = Files.getMtpObjectsUri(originalVolumeName, rowId);
                }
                break;

            case FILES_DIRECTORY:
                rowId = insertDirectory(helper, helper.getWritableDatabase(),
                        initialValues.getAsString(FileColumns.DATA));
                if (rowId > 0) {
                    newUri = Files.getContentUri(originalVolumeName, rowId);
                }
                break;

            case DOWNLOADS:
                maybePut(initialValues, FileColumns.OWNER_PACKAGE_NAME, ownerPackageName);
                initialValues.put(FileColumns.IS_DOWNLOAD, true);
                rowId = insertFile(helper, match, uri, initialValues,
                        FileColumns.MEDIA_TYPE_NONE, false);
                if (rowId > 0) {
                    final int mediaType = initialValues.getAsInteger(FileColumns.MEDIA_TYPE);
                    MediaDocumentsProvider.onMediaStoreInsert(
                            getContext(), resolvedVolumeName, mediaType, rowId);
                    newUri = ContentUris.withAppendedId(
                        MediaStore.Downloads.getContentUri(originalVolumeName), rowId);
                }
                break;

            default:
                throw new UnsupportedOperationException("Invalid URI " + uri);
        }

        // Remember that caller is owner of this item, to speed up future
        // permission checks for this caller
        mCallingIdentity.get().setOwned(rowId, true);

        if (path != null && path.toLowerCase(Locale.US).endsWith("/.nomedia")) {
            MediaScanner.instance(getContext()).scanFile(new File(path).getParentFile());
        }

        if (newUri != null) {
            acceptWithExpansion(helper::notifyChange, newUri);
        }
        return newUri;
    }

    @Override
    public ContentProviderResult[] applyBatch(ArrayList<ContentProviderOperation> operations)
                throws OperationApplicationException {
        // Open transactions on databases for requested volumes
        final ArrayMap<String, DatabaseHelper> transactions = new ArrayMap<>();
        try {
            for (ContentProviderOperation op : operations) {
                final String volumeName = MediaStore.getVolumeName(op.getUri());
                if (!transactions.containsKey(volumeName)) {
                    try {
                        final DatabaseHelper helper = getDatabaseForUri(op.getUri());
                        helper.beginTransaction();
                        transactions.put(volumeName, helper);
                    } catch (VolumeNotFoundException e) {
                        Log.w(TAG, e.getMessage());
                    }
                }
            }

            final ContentProviderResult[] result = super.applyBatch(operations);
            for (DatabaseHelper helper : transactions.values()) {
                helper.setTransactionSuccessful();
            }
            return result;
        } finally {
            for (DatabaseHelper helper : transactions.values()) {
                helper.endTransaction();
            }
        }
    }

    private static void appendWhereStandalone(@NonNull SQLiteQueryBuilder qb,
            @Nullable String selection, @Nullable Object... selectionArgs) {
        qb.appendWhereStandalone(DatabaseUtils.bindSelection(selection, selectionArgs));
    }

    static @NonNull String bindList(@NonNull Object... args) {
        final StringBuilder sb = new StringBuilder();
        sb.append('(');
        for (int i = 0; i < args.length; i++) {
            sb.append('?');
            if (i < args.length - 1) {
                sb.append(',');
            }
        }
        sb.append(')');
        return DatabaseUtils.bindSelection(sb.toString(), args);
    }

    private static boolean parseBoolean(String value) {
        if (value == null) return false;
        if ("1".equals(value)) return true;
        if ("true".equalsIgnoreCase(value)) return true;
        return false;
    }

    @Deprecated
    private String getSharedPackages(String callingPackage) {
        final String[] sharedPackageNames = mCallingIdentity.get().getSharedPackageNames();
        return bindList((Object[]) sharedPackageNames);
    }

    private static final int TYPE_QUERY = 0;
    private static final int TYPE_UPDATE = 1;
    private static final int TYPE_DELETE = 2;

    /**
     * Generate a {@link SQLiteQueryBuilder} that is filtered based on the
     * runtime permissions and/or {@link Uri} grants held by the caller.
     * <ul>
     * <li>If caller holds a {@link Uri} grant, access is allowed according to
     * that grant.
     * <li>If caller holds the write permission for a collection, they can
     * read/write all contents of that collection.
     * <li>If caller holds the read permission for a collection, they can read
     * all contents of that collection, but writes are limited to content they
     * own.
     * <li>If caller holds no permissions for a collection, all reads/write are
     * limited to content they own.
     * </ul>
     */
    private SQLiteQueryBuilder getQueryBuilder(int type, Uri uri, int match, Bundle queryArgs) {
        Trace.traceBegin(TRACE_TAG_DATABASE, "getQueryBuilder");
        try {
            return getQueryBuilderInternal(type, uri, match, queryArgs);
        } finally {
            Trace.traceEnd(TRACE_TAG_DATABASE);
        }
    }

    private SQLiteQueryBuilder getQueryBuilderInternal(int type, Uri uri, int match,
            Bundle queryArgs) {
        final boolean forWrite;
        switch (type) {
            case TYPE_QUERY: forWrite = false; break;
            case TYPE_UPDATE: forWrite = true; break;
            case TYPE_DELETE: forWrite = true; break;
            default: throw new IllegalStateException();
        }

        final SQLiteQueryBuilder qb = new SQLiteQueryBuilder();
        if (parseBoolean(uri.getQueryParameter("distinct"))) {
            qb.setDistinct(true);
        }
        qb.setProjectionAggregationAllowed(true);
        qb.setStrict(true);

        final String callingPackage = getCallingPackageOrSelf();

        // TODO: throw when requesting a currently unmounted volume
        final String volumeName = MediaStore.getVolumeName(uri);
        final String includeVolumes;
        if (MediaStore.VOLUME_EXTERNAL.equals(volumeName)) {
            includeVolumes = bindList(getExternalVolumeNames().toArray());
        } else {
            includeVolumes = bindList(volumeName);
        }
        final String sharedPackages = getSharedPackages(callingPackage);
        final boolean allowGlobal = checkCallingPermissionGlobal(uri, forWrite);
        final boolean allowLegacy = checkCallingPermissionLegacy(uri, forWrite, callingPackage);
        final boolean allowLegacyRead = allowLegacy && !forWrite;

        boolean includePending = parseBoolean(
                uri.getQueryParameter(MediaStore.PARAM_INCLUDE_PENDING));
        boolean includeTrashed = parseBoolean(
                uri.getQueryParameter(MediaStore.PARAM_INCLUDE_TRASHED));
        boolean includeAllVolumes = false;

        switch (match) {
            case IMAGES_MEDIA_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(3));
                includePending = true;
                includeTrashed = true;
                // fall-through
            case IMAGES_MEDIA:
                if (type == TYPE_QUERY) {
                    qb.setTables("images");
                    qb.setProjectionMap(getProjectionMap(Images.Media.class));
                } else {
                    qb.setTables("files");
                    appendWhereStandalone(qb, FileColumns.MEDIA_TYPE + "=?",
                            FileColumns.MEDIA_TYPE_IMAGE);
                }
                if (!allowGlobal && !checkCallingPermissionImages(forWrite, callingPackage)) {
                    appendWhereStandalone(qb, FileColumns.OWNER_PACKAGE_NAME + " IN "
                            + sharedPackages);
                }
                if (!includePending) {
                    appendWhereStandalone(qb, FileColumns.IS_PENDING + "=?", 0);
                }
                if (!includeTrashed) {
                    appendWhereStandalone(qb, FileColumns.IS_TRASHED + "=?", 0);
                }
                if (!includeAllVolumes) {
                    appendWhereStandalone(qb, FileColumns.VOLUME_NAME + " IN " + includeVolumes);
                }
                break;

            case IMAGES_THUMBNAILS_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(3));
                // fall-through
            case IMAGES_THUMBNAILS: {
                qb.setTables("thumbnails");

                final ArrayMap<String, String> projectionMap = new ArrayMap<>(
                        getProjectionMap(Images.Thumbnails.class));
                projectionMap.put(Images.Thumbnails.THUMB_DATA,
                        "NULL AS " + Images.Thumbnails.THUMB_DATA);
                qb.setProjectionMap(projectionMap);

                if (!allowGlobal && !checkCallingPermissionImages(forWrite, callingPackage)) {
                    appendWhereStandalone(qb,
                            "image_id IN (SELECT _id FROM images WHERE owner_package_name IN "
                                    + sharedPackages + ")");
                }
                break;
            }

            case AUDIO_MEDIA_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(3));
                includePending = true;
                includeTrashed = true;
                // fall-through
            case AUDIO_MEDIA:
                if (type == TYPE_QUERY) {
                    qb.setTables("audio");
                    qb.setProjectionMap(getProjectionMap(Audio.Media.class));
                } else {
                    qb.setTables("files");
                    appendWhereStandalone(qb, FileColumns.MEDIA_TYPE + "=?",
                            FileColumns.MEDIA_TYPE_AUDIO);
                }
                if (!allowGlobal && !checkCallingPermissionAudio(forWrite, callingPackage)) {
                    // Apps without Audio permission can only see their own
                    // media, but we also let them see ringtone-style media to
                    // support legacy use-cases.
                    appendWhereStandalone(qb,
                            DatabaseUtils.bindSelection(FileColumns.OWNER_PACKAGE_NAME
                                    + " IN " + sharedPackages
                                    + " OR is_ringtone=1 OR is_alarm=1 OR is_notification=1"));
                }
                if (!includePending) {
                    appendWhereStandalone(qb, FileColumns.IS_PENDING + "=?", 0);
                }
                if (!includeTrashed) {
                    appendWhereStandalone(qb, FileColumns.IS_TRASHED + "=?", 0);
                }
                if (!includeAllVolumes) {
                    appendWhereStandalone(qb, FileColumns.VOLUME_NAME + " IN " + includeVolumes);
                }
                break;

            case AUDIO_MEDIA_ID_GENRES_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(5));
                // fall-through
            case AUDIO_MEDIA_ID_GENRES:
                qb.setTables("audio_genres");
                qb.setProjectionMap(getProjectionMap(Audio.Genres.class));
                appendWhereStandalone(qb, "_id IN (SELECT genre_id FROM " +
                        "audio_genres_map WHERE audio_id=?)", uri.getPathSegments().get(3));
                if (!allowGlobal && !checkCallingPermissionAudio(false, callingPackage)) {
                    // We don't have a great way to filter parsed metadata by
                    // owner, so callers need to hold READ_MEDIA_AUDIO
                    appendWhereStandalone(qb, "0");
                }
                break;

            case AUDIO_MEDIA_ID_PLAYLISTS_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(5));
                // fall-through
            case AUDIO_MEDIA_ID_PLAYLISTS:
                qb.setTables("audio_playlists");
                qb.setProjectionMap(getProjectionMap(Audio.Playlists.class));
                appendWhereStandalone(qb, "_id IN (SELECT playlist_id FROM " +
                        "audio_playlists_map WHERE audio_id=?)", uri.getPathSegments().get(3));
                if (!allowGlobal && !checkCallingPermissionAudio(false, callingPackage)) {
                    // We don't have a great way to filter parsed metadata by
                    // owner, so callers need to hold READ_MEDIA_AUDIO
                    appendWhereStandalone(qb, "0");
                }
                break;

            case AUDIO_GENRES_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(3));
                // fall-through
            case AUDIO_GENRES:
                qb.setTables("audio_genres");
                qb.setProjectionMap(getProjectionMap(Audio.Genres.class));
                if (!allowGlobal && !checkCallingPermissionAudio(false, callingPackage)) {
                    // We don't have a great way to filter parsed metadata by
                    // owner, so callers need to hold READ_MEDIA_AUDIO
                    appendWhereStandalone(qb, "0");
                }
                break;

            case AUDIO_GENRES_ID_MEMBERS:
                appendWhereStandalone(qb, "genre_id=?", uri.getPathSegments().get(3));
                // fall-through
            case AUDIO_GENRES_ALL_MEMBERS:
                if (type == TYPE_QUERY) {
                    qb.setTables("audio_genres_map_noid, audio");
                    qb.setProjectionMap(getProjectionMap(Audio.Genres.Members.class));
                    appendWhereStandalone(qb, "audio._id = audio_id");
                } else {
                    qb.setTables("audio_genres_map");
                }
                if (!allowGlobal && !checkCallingPermissionAudio(false, callingPackage)) {
                    // We don't have a great way to filter parsed metadata by
                    // owner, so callers need to hold READ_MEDIA_AUDIO
                    appendWhereStandalone(qb, "0");
                }
                break;

            case AUDIO_PLAYLISTS_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(3));
                includePending = true;
                includeTrashed = true;
                // fall-through
            case AUDIO_PLAYLISTS:
                if (type == TYPE_QUERY) {
                    qb.setTables("audio_playlists");
                    qb.setProjectionMap(getProjectionMap(Audio.Playlists.class));
                } else {
                    qb.setTables("files");
                    appendWhereStandalone(qb, FileColumns.MEDIA_TYPE + "=?",
                            FileColumns.MEDIA_TYPE_PLAYLIST);
                }
                if (!allowGlobal && !checkCallingPermissionAudio(forWrite, callingPackage)) {
                    appendWhereStandalone(qb, FileColumns.OWNER_PACKAGE_NAME + " IN "
                            + sharedPackages);
                }
                if (!includePending) {
                    appendWhereStandalone(qb, FileColumns.IS_PENDING + "=?", 0);
                }
                if (!includeTrashed) {
                    appendWhereStandalone(qb, FileColumns.IS_TRASHED + "=?", 0);
                }
                if (!includeAllVolumes) {
                    appendWhereStandalone(qb, FileColumns.VOLUME_NAME + " IN " + includeVolumes);
                }
                break;

            case AUDIO_PLAYLISTS_ID_MEMBERS_ID:
                appendWhereStandalone(qb, "audio_playlists_map._id=?",
                        uri.getPathSegments().get(5));
                // fall-through
            case AUDIO_PLAYLISTS_ID_MEMBERS: {
                appendWhereStandalone(qb, "playlist_id=?", uri.getPathSegments().get(3));
                if (type == TYPE_QUERY) {
                    qb.setTables("audio_playlists_map, audio");

                    final ArrayMap<String, String> projectionMap = new ArrayMap<>(
                            getProjectionMap(Audio.Playlists.Members.class));
                    projectionMap.put(Audio.Playlists.Members._ID,
                            "audio_playlists_map._id AS " + Audio.Playlists.Members._ID);
                    qb.setProjectionMap(projectionMap);

                    appendWhereStandalone(qb, "audio._id = audio_id");
                } else {
                    qb.setTables("audio_playlists_map");
                }
                if (!allowGlobal && !checkCallingPermissionAudio(false, callingPackage)) {
                    // We don't have a great way to filter parsed metadata by
                    // owner, so callers need to hold READ_MEDIA_AUDIO
                    appendWhereStandalone(qb, "0");
                }
                break;
            }

            case AUDIO_ALBUMART_ID:
                appendWhereStandalone(qb, "album_id=?", uri.getPathSegments().get(3));
                // fall-through
            case AUDIO_ALBUMART: {
                qb.setTables("album_art");

                final ArrayMap<String, String> projectionMap = new ArrayMap<>(
                        getProjectionMap(Audio.Thumbnails.class));
                projectionMap.put(Audio.Thumbnails._ID,
                        "album_id AS " + Audio.Thumbnails._ID);
                qb.setProjectionMap(projectionMap);

                if (!allowGlobal && !checkCallingPermissionAudio(false, callingPackage)) {
                    // We don't have a great way to filter parsed metadata by
                    // owner, so callers need to hold READ_MEDIA_AUDIO
                    appendWhereStandalone(qb, "0");
                }
                break;
            }
            case AUDIO_ARTISTS_ID_ALBUMS: {
                if (type == TYPE_QUERY) {
                    final String artistId = uri.getPathSegments().get(3);
                    qb.setTables("audio LEFT OUTER JOIN album_art ON" +
                            " audio.album_id=album_art.album_id");
                    appendWhereStandalone(qb,
                            "is_music=1 AND audio.album_id IN (SELECT album_id FROM " +
                                    "artists_albums_map WHERE artist_id=?)", artistId);

                    final ArrayMap<String, String> projectionMap = new ArrayMap<>(
                            getProjectionMap(Audio.Artists.Albums.class));
                    projectionMap.put(Audio.Artists.Albums.ALBUM_ART,
                            "album_art._data AS " + Audio.Artists.Albums.ALBUM_ART);
                    projectionMap.put(Audio.Artists.Albums.NUMBER_OF_SONGS,
                            "count(*) AS " + Audio.Artists.Albums.NUMBER_OF_SONGS);
                    projectionMap.put(Audio.Artists.Albums.NUMBER_OF_SONGS_FOR_ARTIST,
                            "count(CASE WHEN artist_id==" + artistId
                                    + " THEN 'foo' ELSE NULL END) AS "
                                    + Audio.Artists.Albums.NUMBER_OF_SONGS_FOR_ARTIST);
                    projectionMap.put(Audio.Artists.Albums.FIRST_YEAR,
                            "MIN(year) AS " + Audio.Artists.Albums.FIRST_YEAR);
                    projectionMap.put(Audio.Artists.Albums.LAST_YEAR,
                            "MAX(year) AS " + Audio.Artists.Albums.LAST_YEAR);
                    projectionMap.put(Audio.Artists.Albums.ALBUM_ID,
                            "audio.album_id AS " + Audio.Artists.Albums.ALBUM_ID);
                    qb.setProjectionMap(projectionMap);
                } else {
                    throw new UnsupportedOperationException("Albums cannot be directly modified");
                }
                if (!allowGlobal && !checkCallingPermissionAudio(false, callingPackage)) {
                    // We don't have a great way to filter parsed metadata by
                    // owner, so callers need to hold READ_MEDIA_AUDIO
                    appendWhereStandalone(qb, "0");
                }
                break;
            }

            case AUDIO_ARTISTS_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(3));
                // fall-through
            case AUDIO_ARTISTS:
                if (type == TYPE_QUERY) {
                    qb.setTables("artist_info");
                    qb.setProjectionMap(getProjectionMap(Audio.Artists.class));
                } else {
                    throw new UnsupportedOperationException("Artists cannot be directly modified");
                }
                if (!allowGlobal && !checkCallingPermissionAudio(false, callingPackage)) {
                    // We don't have a great way to filter parsed metadata by
                    // owner, so callers need to hold READ_MEDIA_AUDIO
                    appendWhereStandalone(qb, "0");
                }
                break;

            case AUDIO_ALBUMS_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(3));
                // fall-through
            case AUDIO_ALBUMS: {
                if (type == TYPE_QUERY) {
                    qb.setTables("album_info");

                    final ArrayMap<String, String> projectionMap = new ArrayMap<>(
                            getProjectionMap(Audio.Albums.class));
                    projectionMap.put(Audio.Artists.Albums.NUMBER_OF_SONGS_FOR_ARTIST,
                            "NULL AS " + Audio.Artists.Albums.NUMBER_OF_SONGS_FOR_ARTIST);
                    projectionMap.put(Audio.Artists.Albums.ALBUM_ID,
                            BaseColumns._ID + " AS " + Audio.Artists.Albums.ALBUM_ID);
                    qb.setProjectionMap(projectionMap);
                } else {
                    throw new UnsupportedOperationException("Albums cannot be directly modified");
                }
                if (!allowGlobal && !checkCallingPermissionAudio(false, callingPackage)) {
                    // We don't have a great way to filter parsed metadata by
                    // owner, so callers need to hold READ_MEDIA_AUDIO
                    appendWhereStandalone(qb, "0");
                }
                break;
            }

            case VIDEO_MEDIA_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(3));
                includePending = true;
                includeTrashed = true;
                // fall-through
            case VIDEO_MEDIA:
                if (type == TYPE_QUERY) {
                    qb.setTables("video");
                    qb.setProjectionMap(getProjectionMap(Video.Media.class));
                } else {
                    qb.setTables("files");
                    appendWhereStandalone(qb, FileColumns.MEDIA_TYPE + "=?",
                            FileColumns.MEDIA_TYPE_VIDEO);
                }
                if (!allowGlobal && !checkCallingPermissionVideo(forWrite, callingPackage)) {
                    appendWhereStandalone(qb, FileColumns.OWNER_PACKAGE_NAME + " IN "
                            + sharedPackages);
                }
                if (!includePending) {
                    appendWhereStandalone(qb, FileColumns.IS_PENDING + "=?", 0);
                }
                if (!includeTrashed) {
                    appendWhereStandalone(qb, FileColumns.IS_TRASHED + "=?", 0);
                }
                if (!includeAllVolumes) {
                    appendWhereStandalone(qb, FileColumns.VOLUME_NAME + " IN " + includeVolumes);
                }
                break;

            case VIDEO_THUMBNAILS_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(3));
                // fall-through
            case VIDEO_THUMBNAILS:
                qb.setTables("videothumbnails");
                qb.setProjectionMap(getProjectionMap(Video.Thumbnails.class));
                if (!allowGlobal && !checkCallingPermissionVideo(forWrite, callingPackage)) {
                    appendWhereStandalone(qb,
                            "video_id IN (SELECT _id FROM video WHERE owner_package_name IN "
                                    + sharedPackages + ")");
                }
                break;

            case FILES_ID:
            case MTP_OBJECTS_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(2));
                includePending = true;
                includeTrashed = true;
                // fall-through
            case FILES:
            case FILES_DIRECTORY:
            case MTP_OBJECTS: {
                qb.setTables("files");
                qb.setProjectionMap(getProjectionMap(Files.FileColumns.class));

                final ArrayList<String> options = new ArrayList<>();
                if (!allowGlobal && !allowLegacyRead) {
                    options.add(DatabaseUtils.bindSelection("owner_package_name IN "
                            + sharedPackages));
                    if (allowLegacy) {
                        options.add(DatabaseUtils.bindSelection("volume_name=?",
                                MediaStore.VOLUME_EXTERNAL_PRIMARY));
                    }
                    if (checkCallingPermissionAudio(forWrite, callingPackage)) {
                        options.add(DatabaseUtils.bindSelection("media_type=?",
                                FileColumns.MEDIA_TYPE_AUDIO));
                        options.add(DatabaseUtils.bindSelection("media_type=?",
                                FileColumns.MEDIA_TYPE_PLAYLIST));
                        options.add("media_type=0 AND mime_type LIKE 'audio/%'");
                    }
                    if (checkCallingPermissionVideo(forWrite, callingPackage)) {
                        options.add(DatabaseUtils.bindSelection("media_type=?",
                                FileColumns.MEDIA_TYPE_VIDEO));
                        options.add("media_type=0 AND mime_type LIKE 'video/%'");
                    }
                    if (checkCallingPermissionImages(forWrite, callingPackage)) {
                        options.add(DatabaseUtils.bindSelection("media_type=?",
                                FileColumns.MEDIA_TYPE_IMAGE));
                        options.add("media_type=0 AND mime_type LIKE 'image/%'");
                    }
                }
                if (options.size() > 0) {
                    appendWhereStandalone(qb, TextUtils.join(" OR ", options));
                }

                if (!includePending) {
                    appendWhereStandalone(qb, FileColumns.IS_PENDING + "=?", 0);
                }
                if (!includeTrashed) {
                    appendWhereStandalone(qb, FileColumns.IS_TRASHED + "=?", 0);
                }
                if (!includeAllVolumes) {
                    appendWhereStandalone(qb, FileColumns.VOLUME_NAME + " IN " + includeVolumes);
                }
                break;
            }
            case DOWNLOADS_ID:
                appendWhereStandalone(qb, "_id=?", uri.getPathSegments().get(2));
                includePending = true;
                includeTrashed = true;
                // fall-through
            case DOWNLOADS: {
                if (type == TYPE_QUERY) {
                    qb.setTables("downloads");
                    qb.setProjectionMap(getProjectionMap(Downloads.class));
                } else {
                    qb.setTables("files");
                    appendWhereStandalone(qb, FileColumns.IS_DOWNLOAD + "=1");
                }

                final ArrayList<String> options = new ArrayList<>();
                if (!allowGlobal && !allowLegacyRead) {
                    options.add(DatabaseUtils.bindSelection("owner_package_name IN "
                            + sharedPackages));
                    if (allowLegacy) {
                        options.add(DatabaseUtils.bindSelection("volume_name=?",
                                MediaStore.VOLUME_EXTERNAL_PRIMARY));
                    }
                }
                if (options.size() > 0) {
                    appendWhereStandalone(qb, TextUtils.join(" OR ", options));
                }

                if (!includePending) {
                    appendWhereStandalone(qb, FileColumns.IS_PENDING + "=?", 0);
                }
                if (!includeTrashed) {
                    appendWhereStandalone(qb, FileColumns.IS_TRASHED + "=?", 0);
                }
                if (!includeAllVolumes) {
                    appendWhereStandalone(qb, FileColumns.VOLUME_NAME + " IN " + includeVolumes);
                }
                break;
            }
            default:
                throw new UnsupportedOperationException(
                        "Unknown or unsupported URL: " + uri.toString());
        }

        if (type == TYPE_QUERY) {
            // To ensure we're enforcing our security model, all queries must
            // have a projection map configured
            if (qb.getProjectionMap() == null) {
                throw new IllegalStateException("All queries must have a projection map");
            }

            // If caller is an older app, we're willing to let through a
            // greylist of technically invalid columns
            if (getCallingPackageTargetSdkVersion() < Build.VERSION_CODES.Q) {
                qb.setProjectionGreylist(sGreylist);
            }
        }

        return qb;
    }

    /**
     * Determine if given {@link Uri} has a
     * {@link MediaColumns#OWNER_PACKAGE_NAME} column.
     */
    private static boolean hasOwnerPackageName(Uri uri) {
        // It's easier to maintain this as an inverted list
        final int table = matchUri(uri, true);
        switch (table) {
            case IMAGES_THUMBNAILS_ID:
            case IMAGES_THUMBNAILS:
            case VIDEO_THUMBNAILS_ID:
            case VIDEO_THUMBNAILS:
            case AUDIO_ALBUMART:
            case AUDIO_ALBUMART_ID:
            case AUDIO_ALBUMART_FILE_ID:
                return false;
            default:
                return true;
        }
    }

    @Override
    public int delete(Uri uri, String userWhere, String[] userWhereArgs) {
        Trace.traceBegin(TRACE_TAG_DATABASE, "insert");
        try {
            return deleteInternal(uri, userWhere, userWhereArgs);
        } finally {
            Trace.traceEnd(TRACE_TAG_DATABASE);
        }
    }

    private int deleteInternal(Uri uri, String userWhere, String[] userWhereArgs) {
        uri = safeUncanonicalize(uri);

        int count;

        final String volumeName = getVolumeName(uri);
        final int targetSdkVersion = getCallingPackageTargetSdkVersion();
        final boolean allowHidden = isCallingPackageAllowedHidden();
        final int match = matchUri(uri, allowHidden);

        // handle MEDIA_SCANNER before calling getDatabaseForUri()
        if (match == MEDIA_SCANNER) {
            if (mMediaScannerVolume == null) {
                return 0;
            }

            final DatabaseHelper helper;
            try {
                helper = getDatabaseForUri(MediaStore.Files.getContentUri(mMediaScannerVolume));
            } catch (VolumeNotFoundException e) {
                return e.translateForUpdateDelete(targetSdkVersion);
            }

            helper.mScanStopTime = SystemClock.currentTimeMicro();
            String msg = dump(helper, false);
            logToDb(helper.getWritableDatabase(), msg);

            if (MediaStore.VOLUME_INTERNAL.equals(mMediaScannerVolume)) {
                // persist current build fingerprint as fingerprint for system (internal) sound scan
                final SharedPreferences scanSettings = getContext().getSharedPreferences(
                        android.media.MediaScanner.SCANNED_BUILD_PREFS_NAME,
                        Context.MODE_PRIVATE);
                final SharedPreferences.Editor editor = scanSettings.edit();
                editor.putString(android.media.MediaScanner.LAST_INTERNAL_SCAN_FINGERPRINT,
                        Build.FINGERPRINT);
                editor.apply();
            }
            mMediaScannerVolume = null;
            return 1;
        }

        if (match == VOLUMES_ID) {
            detachVolume(uri);
            count = 1;
        }

        final DatabaseHelper helper;
        final SQLiteDatabase db;
        try {
            helper = getDatabaseForUri(uri);
            db = helper.getWritableDatabase();
        } catch (VolumeNotFoundException e) {
            return e.translateForUpdateDelete(targetSdkVersion);
        }

        {
            final SQLiteQueryBuilder qb = getQueryBuilder(TYPE_DELETE, uri, match, null);

            // Give callers interacting with a specific media item a chance to
            // escalate access if they don't already have it
            switch (match) {
                case AUDIO_MEDIA_ID:
                case VIDEO_MEDIA_ID:
                case IMAGES_MEDIA_ID:
                    enforceCallingPermission(uri, true);
            }

            final String[] projection = new String[] {
                    FileColumns.MEDIA_TYPE,
                    FileColumns.DATA,
                    FileColumns._ID,
                    FileColumns.IS_DOWNLOAD,
                    FileColumns.MIME_TYPE,
            };
            final LongSparseArray<String> deletedDownloadIds = new LongSparseArray<>();
            if (qb.getTables().equals("files")) {
                String deleteparam = uri.getQueryParameter(MediaStore.PARAM_DELETE_DATA);
                if (deleteparam == null || ! deleteparam.equals("false")) {
                    Cursor c = qb.query(db, projection, userWhere, userWhereArgs,
                            null, null, null, null);
                    String [] idvalue = new String[] { "" };
                    String [] playlistvalues = new String[] { "", "" };
                    try {
                        while (c.moveToNext()) {
                            final int mediaType = c.getInt(0);
                            final String data = c.getString(1);
                            final long id = c.getLong(2);
                            final int isDownload = c.getInt(3);
                            final String mimeType = c.getString(4);

                            // Forget that caller is owner of this item
                            mCallingIdentity.get().setOwned(id, false);

                            // Invalidate thumbnails and revoke all outstanding grants
                            final Uri deletedUri = Files.getContentUri(volumeName, id);
                            invalidateThumbnails(deletedUri);
                            acceptWithExpansion((expandedUri) -> {
                                getContext().revokeUriPermission(expandedUri,
                                        Intent.FLAG_GRANT_READ_URI_PERMISSION
                                                | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
                            }, deletedUri);

                            // Only need to inform DownloadProvider about the downloads deleted on
                            // external volume.
                            if (isDownload == 1) {
                                deletedDownloadIds.put(id, mimeType);
                            }
                            if (mediaType == FileColumns.MEDIA_TYPE_IMAGE) {
                                deleteIfAllowed(uri, data);
                                MediaDocumentsProvider.onMediaStoreDelete(getContext(),
                                        volumeName, FileColumns.MEDIA_TYPE_IMAGE, id);
                            } else if (mediaType == FileColumns.MEDIA_TYPE_VIDEO) {
                                deleteIfAllowed(uri, data);
                                MediaDocumentsProvider.onMediaStoreDelete(getContext(),
                                        volumeName, FileColumns.MEDIA_TYPE_VIDEO, id);
                            } else if (mediaType == FileColumns.MEDIA_TYPE_AUDIO) {
                                if (!helper.mInternal) {
                                    deleteIfAllowed(uri, data);
                                    MediaDocumentsProvider.onMediaStoreDelete(getContext(),
                                            volumeName, FileColumns.MEDIA_TYPE_AUDIO, id);

                                    idvalue[0] = String.valueOf(id);
                                    db.delete("audio_genres_map", "audio_id=?", idvalue);
                                    // for each playlist that the item appears in, move
                                    // all the items behind it forward by one
                                    Cursor cc = db.query("audio_playlists_map",
                                                sPlaylistIdPlayOrder,
                                                "audio_id=?", idvalue, null, null, null);
                                    try {
                                        while (cc.moveToNext()) {
                                            long playlistId = cc.getLong(0);
                                            playlistvalues[0] = String.valueOf(playlistId);
                                            playlistvalues[1] = String.valueOf(cc.getInt(1));
                                            int rowsChanged = db.executeSql("UPDATE audio_playlists_map" +
                                                    " SET play_order=play_order-1" +
                                                    " WHERE playlist_id=? AND play_order>?",
                                                    playlistvalues);

                                            if (rowsChanged > 0) {
                                                updatePlaylistDateModifiedToNow(db, playlistId);
                                            }
                                        }
                                        db.delete("audio_playlists_map", "audio_id=?", idvalue);
                                    } finally {
                                        IoUtils.closeQuietly(cc);
                                    }
                                }
                            } else if (isDownload == 1) {
                                deleteIfAllowed(uri, data);
                                MediaDocumentsProvider.onMediaStoreDelete(getContext(),
                                        volumeName, mediaType, id);
                            } else if (mediaType == FileColumns.MEDIA_TYPE_PLAYLIST) {
                                // TODO, maybe: remove the audio_playlists_cleanup trigger and
                                // implement functionality here (clean up the playlist map)
                            }
                        }
                    } finally {
                        IoUtils.closeQuietly(c);
                    }
                    // Do not allow deletion if the file/object is referenced as parent
                    // by some other entries. It could cause database corruption.
                    appendWhereStandalone(qb, ID_NOT_PARENT_CLAUSE);
                }
            }

            switch (match) {
                case MTP_OBJECTS:
                case MTP_OBJECTS_ID:
                    count = deleteRecursive(qb, db, userWhere, userWhereArgs);
                    break;
                case AUDIO_GENRES_ID_MEMBERS:
                    count = deleteRecursive(qb, db, userWhere, userWhereArgs);
                    break;

                case IMAGES_THUMBNAILS_ID:
                case IMAGES_THUMBNAILS:
                case VIDEO_THUMBNAILS_ID:
                case VIDEO_THUMBNAILS:
                    // Delete the referenced files first.
                    Cursor c = qb.query(db, sDataOnlyColumn, userWhere, userWhereArgs, null, null,
                            null, null);
                    if (c != null) {
                        try {
                            while (c.moveToNext()) {
                                deleteIfAllowed(uri, c.getString(0));
                            }
                        } finally {
                            IoUtils.closeQuietly(c);
                        }
                    }
                    count = deleteRecursive(qb, db, userWhere, userWhereArgs);
                    break;

                case AUDIO_PLAYLISTS_ID_MEMBERS_ID:
                    long playlistId = Long.parseLong(uri.getPathSegments().get(3));
                    count = deleteRecursive(qb, db, userWhere, userWhereArgs);
                    if (count > 0) {
                        updatePlaylistDateModifiedToNow(db, playlistId);
                    }
                    break;
                default:
                    count = deleteRecursive(qb, db, userWhere, userWhereArgs);
                    break;
            }

            if (deletedDownloadIds.size() > 0) {
                final long token = Binder.clearCallingIdentity();
                try (ContentProviderClient client = getContext().getContentResolver()
                     .acquireUnstableContentProviderClient(
                             android.provider.Downloads.Impl.AUTHORITY)) {
                    final Bundle extras = new Bundle();
                    final long[] ids = new long[deletedDownloadIds.size()];
                    final String[] mimeTypes = new String[deletedDownloadIds.size()];
                    for (int i = deletedDownloadIds.size() - 1; i >= 0; --i) {
                        ids[i] = deletedDownloadIds.keyAt(i);
                        mimeTypes[i] = deletedDownloadIds.valueAt(i);
                    }
                    extras.putLongArray(android.provider.Downloads.EXTRA_IDS, ids);
                    extras.putStringArray(android.provider.Downloads.EXTRA_MIME_TYPES, mimeTypes);
                    client.call(android.provider.Downloads.CALL_MEDIASTORE_DOWNLOADS_DELETED,
                            null, extras);
                } catch (RemoteException e) {
                    // Should not happen
                } finally {
                    Binder.restoreCallingIdentity(token);
                }
            }
        }

        if (count > 0) {
            acceptWithExpansion(helper::notifyChange, uri);
        }
        return count;
    }

    /**
     * Executes identical delete repeatedly within a single transaction until
     * stability is reached. Combined with {@link #ID_NOT_PARENT_CLAUSE}, this
     * can be used to recursively delete all matching entries, since it only
     * deletes parents when no references remaining.
     */
    private int deleteRecursive(SQLiteQueryBuilder qb, SQLiteDatabase db, String userWhere,
            String[] userWhereArgs) {
        db.beginTransaction();
        try {
            int n = 0;
            int total = 0;
            do {
                n = qb.delete(db, userWhere, userWhereArgs);
                total += n;
            } while (n > 0);
            db.setTransactionSuccessful();
            return total;
        } finally {
            db.endTransaction();
        }
    }

    @Override
    public Bundle call(String method, String arg, Bundle extras) {
        switch (method) {
            case MediaStore.SCAN_FILE_CALL: {
                final LocalCallingIdentity token = clearLocalCallingIdentity();
                final CallingIdentity providerToken = clearCallingIdentity();

                final Uri uri;
                try {
                    final Uri fileUri = extras.getParcelable(Intent.EXTRA_STREAM);
                    File file;
                    try {
                        file = getCanonicalFile(fileUri.getPath());
                    } catch (IOException e) {
                        file = null;
                    }

                    uri = file != null ? MediaScanner.instance(getContext()).scanFile(file) : null;
                } finally {
                    restoreCallingIdentity(providerToken);
                    restoreLocalCallingIdentity(token);
                }

                final Bundle res = new Bundle();
                res.putParcelable(Intent.EXTRA_STREAM, uri);
                return res;
            }
            case MediaStore.SCAN_VOLUME_CALL: {
                final LocalCallingIdentity token = clearLocalCallingIdentity();
                final CallingIdentity providerToken = clearCallingIdentity();

                try {
                    final Uri uri = extras.getParcelable(Intent.EXTRA_STREAM);
                    final File file = new File(uri.getPath());
                    MediaService.onScanVolume(getContext(), Uri.fromFile(file));
                } catch (IOException e) {
                    throw new RuntimeException(e);
                } finally {
                    restoreCallingIdentity(providerToken);
                    restoreLocalCallingIdentity(token);
                }
                return Bundle.EMPTY;
            }
            case MediaStore.UNHIDE_CALL: {
                throw new UnsupportedOperationException();
            }
            case MediaStore.RETRANSLATE_CALL: {
                localizeTitles();
                return null;
            }
            case MediaStore.GET_VERSION_CALL: {
                final String volumeName = extras.getString(Intent.EXTRA_TEXT);

                final SQLiteDatabase db;
                try {
                    db = getDatabaseForUri(MediaStore.Files.getContentUri(volumeName))
                            .getReadableDatabase();
                } catch (VolumeNotFoundException e) {
                    throw e.rethrowAsIllegalArgumentException();
                }

                final String version = db.getVersion() + ":" + getOrCreateUuid(db);

                final Bundle res = new Bundle();
                res.putString(Intent.EXTRA_TEXT, version);
                return res;
            }
            case MediaStore.GET_DOCUMENT_URI_CALL: {
                final Uri mediaUri = extras.getParcelable(DocumentsContract.EXTRA_URI);
                enforceCallingPermission(mediaUri, false);

                final Uri fileUri;
                final LocalCallingIdentity token = clearLocalCallingIdentity();
                try {
                    fileUri = Uri.fromFile(queryForDataFile(mediaUri, null));
                } catch (FileNotFoundException e) {
                    throw new IllegalArgumentException(e);
                } finally {
                    restoreLocalCallingIdentity(token);
                }

                try (ContentProviderClient client = getContext().getContentResolver()
                        .acquireUnstableContentProviderClient(
                                DocumentsContract.EXTERNAL_STORAGE_PROVIDER_AUTHORITY)) {
                    extras.putParcelable(DocumentsContract.EXTRA_URI, fileUri);
                    return client.call(method, null, extras);
                } catch (RemoteException e) {
                    throw new IllegalStateException(e);
                }
            }
            case MediaStore.GET_MEDIA_URI_CALL: {
                final Uri documentUri = extras.getParcelable(DocumentsContract.EXTRA_URI);
                getContext().enforceCallingUriPermission(documentUri,
                        Intent.FLAG_GRANT_READ_URI_PERMISSION, TAG);

                final Uri fileUri;
                try (ContentProviderClient client = getContext().getContentResolver()
                        .acquireUnstableContentProviderClient(
                                DocumentsContract.EXTERNAL_STORAGE_PROVIDER_AUTHORITY)) {
                    final Bundle res = client.call(method, null, extras);
                    fileUri = res.getParcelable(DocumentsContract.EXTRA_URI);
                } catch (RemoteException e) {
                    throw new IllegalStateException(e);
                }

                final LocalCallingIdentity token = clearLocalCallingIdentity();
                try {
                    final Bundle res = new Bundle();
                    res.putParcelable(DocumentsContract.EXTRA_URI,
                            queryForMediaUri(new File(fileUri.getPath()), null));
                    return res;
                } catch (FileNotFoundException e) {
                    throw new IllegalArgumentException(e);
                } finally {
                    restoreLocalCallingIdentity(token);
                }
            }
            case MediaStore.GET_CONTRIBUTED_MEDIA_CALL: {
                getContext().enforceCallingOrSelfPermission(
                        android.Manifest.permission.CLEAR_APP_USER_DATA, TAG);

                final String packageName = extras.getString(Intent.EXTRA_PACKAGE_NAME);
                final long totalSize = forEachContributedMedia(packageName, null);
                final Bundle res = new Bundle();
                res.putLong(Intent.EXTRA_INDEX, totalSize);
                return res;
            }
            case MediaStore.DELETE_CONTRIBUTED_MEDIA_CALL: {
                getContext().enforceCallingOrSelfPermission(
                        android.Manifest.permission.CLEAR_APP_USER_DATA, TAG);

                final String packageName = extras.getString(Intent.EXTRA_PACKAGE_NAME);
                forEachContributedMedia(packageName, (uri) -> {
                    delete(uri, null, null);
                });
                return null;
            }
            default:
                throw new UnsupportedOperationException("Unsupported call: " + method);
        }
    }

    /**
     * Execute the given operation for each media item contributed by given
     * package. The meaning of "contributed" means it won't automatically be
     * deleted when the app is uninstalled.
     */
    private @BytesLong long forEachContributedMedia(String packageName, Consumer<Uri> consumer) {
        final DatabaseHelper helper = mExternalDatabase;
        final SQLiteDatabase db = helper.getReadableDatabase();

        final SQLiteQueryBuilder qb = new SQLiteQueryBuilder();
        qb.setTables("files");
        qb.appendWhere(
                DatabaseUtils.bindSelection(FileColumns.OWNER_PACKAGE_NAME + "=?", packageName)
                        + " AND NOT " + FileColumns.DATA + " REGEXP '"
                        + PATTERN_OWNED_PATH.pattern() + "'");

        long totalSize = 0;
        final LocalCallingIdentity token = clearLocalCallingIdentity();
        try {
            try (Cursor c = qb.query(db, new String[] {
                    FileColumns.VOLUME_NAME, FileColumns._ID, FileColumns.SIZE, FileColumns.DATA
            }, null, null, null, null, null, null)) {
                while (c.moveToNext()) {
                    final String volumeName = c.getString(0);
                    final long id = c.getLong(1);
                    final long size = c.getLong(2);
                    final String data = c.getString(3);

                    Log.d(TAG, "Found " + data + " from " + packageName + " in "
                            + helper.mName + " with size " + size);
                    if (consumer != null) {
                        consumer.accept(Files.getContentUri(volumeName, id));
                    }
                    totalSize += size;
                }
            }
        } finally {
            restoreLocalCallingIdentity(token);
        }
        return totalSize;
    }

    private void pruneThumbnails(@NonNull CancellationSignal signal) {
        final DatabaseHelper helper = mExternalDatabase;
        final SQLiteDatabase db = helper.getReadableDatabase();

        // Determine all known media items
        final LongArray knownIds = new LongArray();
        try (Cursor c = db.query(true, "files", new String[] { BaseColumns._ID },
                null, null, null, null, null, null, signal)) {
            while (c.moveToNext()) {
                knownIds.add(c.getLong(0));
            }
        }

        final long[] knownIdsRaw = knownIds.toArray();
        Arrays.sort(knownIdsRaw);

        for (String volumeName : getExternalVolumeNames()) {
            final File volumePath;
            try {
                volumePath = getVolumePath(volumeName);
            } catch (FileNotFoundException e) {
                Log.w(TAG, "Failed to resolve volume " + volumeName, e);
                continue;
            }

            // Reconcile all thumbnails, deleting stale items
            for (File thumbDir : new File[] {
                    buildPath(volumePath, Environment.DIRECTORY_MUSIC, ".thumbnails"),
                    buildPath(volumePath, Environment.DIRECTORY_MOVIES, ".thumbnails"),
                    buildPath(volumePath, Environment.DIRECTORY_PICTURES, ".thumbnails"),
            }) {
                // Possibly bail before digging into each directory
                signal.throwIfCanceled();

                for (File thumbFile : FileUtils.listFilesOrEmpty(thumbDir)) {
                    final String name = ModernMediaScanner.extractName(thumbFile);
                    try {
                        final long id = Long.parseLong(name);
                        if (Arrays.binarySearch(knownIdsRaw, id) >= 0) {
                            // Thumbnail belongs to known media, keep it
                            continue;
                        }
                    } catch (NumberFormatException e) {
                    }

                    Log.v(TAG, "Deleting stale thumbnail " + thumbFile);
                    thumbFile.delete();
                }
            }
        }

        // Also delete stale items from legacy tables
        db.execSQL("delete from thumbnails "
                + "where image_id not in (select _id from images)");
        db.execSQL("delete from videothumbnails "
                + "where video_id not in (select _id from video)");
    }

    static abstract class Thumbnailer {
        final String directoryName;

        public Thumbnailer(String directoryName) {
            this.directoryName = directoryName;
        }

        private File getThumbnailFile(Uri uri) throws IOException {
            final String volumeName = resolveVolumeName(uri);
            final File volumePath = getVolumePath(volumeName);
            return Environment.buildPath(volumePath, directoryName,
                    ".thumbnails", ContentUris.parseId(uri) + ".jpg");
        }

        public abstract Bitmap getThumbnailBitmap(Uri uri, CancellationSignal signal)
                throws IOException;

        public File ensureThumbnail(Uri uri, CancellationSignal signal) throws IOException {
            final File thumbFile = getThumbnailFile(uri);
            thumbFile.getParentFile().mkdirs();
            if (!thumbFile.exists()) {
                final Bitmap thumbnail = getThumbnailBitmap(uri, signal);
                try (OutputStream out = new FileOutputStream(thumbFile)) {
                    thumbnail.compress(Bitmap.CompressFormat.JPEG, 75, out);
                }
            }
            return thumbFile;
        }

        public void invalidateThumbnail(Uri uri) throws IOException {
            getThumbnailFile(uri).delete();
        }
    }

    private Thumbnailer mAudioThumbnailer = new Thumbnailer(Environment.DIRECTORY_MUSIC) {
        @Override
        public Bitmap getThumbnailBitmap(Uri uri, CancellationSignal signal) throws IOException {
            return ThumbnailUtils.createAudioThumbnail(queryForDataFile(uri, signal),
                    mThumbSize, signal);
        }
    };

    private Thumbnailer mVideoThumbnailer = new Thumbnailer(Environment.DIRECTORY_MOVIES) {
        @Override
        public Bitmap getThumbnailBitmap(Uri uri, CancellationSignal signal) throws IOException {
            return ThumbnailUtils.createVideoThumbnail(queryForDataFile(uri, signal),
                    mThumbSize, signal);
        }
    };

    private Thumbnailer mImageThumbnailer = new Thumbnailer(Environment.DIRECTORY_PICTURES) {
        @Override
        public Bitmap getThumbnailBitmap(Uri uri, CancellationSignal signal) throws IOException {
            return ThumbnailUtils.createImageThumbnail(queryForDataFile(uri, signal),
                    mThumbSize, signal);
        }
    };

    private void invalidateThumbnails(Uri uri) {
        Trace.traceBegin(TRACE_TAG_DATABASE, "invalidateThumbnails");
        try {
            invalidateThumbnailsInternal(uri);
        } finally {
            Trace.traceEnd(TRACE_TAG_DATABASE);
        }
    }

    private void invalidateThumbnailsInternal(Uri uri) {
        final long id = ContentUris.parseId(uri);
        try {
            mAudioThumbnailer.invalidateThumbnail(uri);
            mVideoThumbnailer.invalidateThumbnail(uri);
            mImageThumbnailer.invalidateThumbnail(uri);
        } catch (IOException ignored) {
        }

        final DatabaseHelper helper;
        final SQLiteDatabase db;
        try {
            helper = getDatabaseForUri(uri);
            db = helper.getWritableDatabase();
        } catch (VolumeNotFoundException e) {
            Log.w(TAG, e);
            return;
        }

        final String idString = Long.toString(id);
        try (Cursor c = db.rawQuery("select _data from thumbnails where image_id=?"
                + " union all select _data from videothumbnails where video_id=?",
                new String[] { idString, idString })) {
            while (c.moveToNext()) {
                String path = c.getString(0);
                deleteIfAllowed(uri, path);
            }
        }

        db.execSQL("delete from thumbnails where image_id=?", new String[] { idString });
        db.execSQL("delete from videothumbnails where video_id=?", new String[] { idString });
    }

    @Override
    public int update(Uri uri, ContentValues initialValues, String userWhere,
            String[] userWhereArgs) {
        Trace.traceBegin(TRACE_TAG_DATABASE, "update");
        try {
            return updateInternal(uri, initialValues, userWhere, userWhereArgs);
        } finally {
            Trace.traceEnd(TRACE_TAG_DATABASE);
        }
    }

    private int updateInternal(Uri uri, ContentValues initialValues, String userWhere,
            String[] userWhereArgs) {
        if ("com.google.android.GoogleCamera".equals(getCallingPackageOrSelf())) {
            if (matchUri(uri, false) == IMAGES_MEDIA_ID) {
                Log.w(TAG, "Working around app bug in b/111966296");
                uri = MediaStore.Files.getContentUri("external", ContentUris.parseId(uri));
            } else if (matchUri(uri, false) == VIDEO_MEDIA_ID) {
                Log.w(TAG, "Working around app bug in b/112246630");
                uri = MediaStore.Files.getContentUri("external", ContentUris.parseId(uri));
            }
        }

        uri = safeUncanonicalize(uri);

        int count;

        final String volumeName = getVolumeName(uri);
        final int targetSdkVersion = getCallingPackageTargetSdkVersion();
        final boolean allowHidden = isCallingPackageAllowedHidden();
        final int match = matchUri(uri, allowHidden);

        final DatabaseHelper helper;
        final SQLiteDatabase db;
        try {
            helper = getDatabaseForUri(uri);
            db = helper.getWritableDatabase();
        } catch (VolumeNotFoundException e) {
            return e.translateForUpdateDelete(targetSdkVersion);
        }

        final SQLiteQueryBuilder qb = getQueryBuilder(TYPE_UPDATE, uri, match, null);

        // Give callers interacting with a specific media item a chance to
        // escalate access if they don't already have it
        switch (match) {
            case AUDIO_MEDIA_ID:
            case VIDEO_MEDIA_ID:
            case IMAGES_MEDIA_ID:
                enforceCallingPermission(uri, true);
        }

        boolean triggerInvalidate = false;
        boolean triggerScan = false;
        String genre = null;
        if (initialValues != null) {
            // IDs are forever; nobody should be editing them
            initialValues.remove(MediaColumns._ID);

            // Ignore or augment incoming raw filesystem paths
            for (String column : sDataColumns.keySet()) {
                if (!initialValues.containsKey(column)) continue;

                if (isCallingPackageSystem() || isCallingPackageLegacy()) {
                    // Mutation allowed
                } else {
                    Log.w(TAG, "Ignoring mutation of  " + column + " from "
                            + getCallingPackageOrSelf());
                    initialValues.remove(column);
                }
            }

            if (!isCallingPackageSystem()) {
                Trace.traceBegin(TRACE_TAG_DATABASE, "filter");

                // Remote callers have no direct control over owner column; we
                // force it be whoever is creating the content.
                initialValues.remove(MediaColumns.OWNER_PACKAGE_NAME);

                // We default to filtering mutable columns, except when we know
                // the single item being updated is pending; when it's finally
                // published we'll overwrite these values.
                final Uri finalUri = uri;
                final Supplier<Boolean> isPending = new CachedSupplier<>(() -> {
                    return isPending(finalUri);
                });

                // Column values controlled by media scanner aren't writable by
                // apps, since any edits here don't reflect the metadata on
                // disk, and they'd be overwritten during a rescan.
                for (String column : new ArraySet<>(initialValues.keySet())) {
                    if (sMutableColumns.contains(column)) {
                        // Mutation normally allowed
                    } else if (isPending.get()) {
                        // Mutation relaxed while pending
                    } else {
                        Log.w(TAG, "Ignoring mutation of " + column + " from "
                                + getCallingPackageOrSelf());
                        initialValues.remove(column);

                        switch (match) {
                            default:
                                triggerScan = true;
                                break;
                            // If entry is a playlist, do not re-scan to match previous behavior
                            // and allow persistence of database-only edits until real re-scan
                            case AUDIO_MEDIA_ID_PLAYLISTS_ID:
                            case AUDIO_PLAYLISTS_ID:
                                break;
                        }
                    }

                    // If we're publishing this item, perform a blocking scan to
                    // make sure metadata is updated
                    if (MediaColumns.IS_PENDING.equals(column)) {
                        triggerScan = true;
                    }
                }

                Trace.traceEnd(TRACE_TAG_DATABASE);
            }

            genre = initialValues.getAsString(Audio.AudioColumns.GENRE);
            initialValues.remove(Audio.AudioColumns.GENRE);

            if ("files".equals(qb.getTables())) {
                maybeMarkAsDownload(initialValues);
            }

            // We no longer track location metadata
            if (initialValues.containsKey(ImageColumns.LATITUDE)) {
                initialValues.putNull(ImageColumns.LATITUDE);
            }
            if (initialValues.containsKey(ImageColumns.LONGITUDE)) {
                initialValues.putNull(ImageColumns.LONGITUDE);
            }
        }

        // If we're not updating anything, then we can skip
        if (initialValues.isEmpty()) return 0;

        final boolean isThumbnail;
        switch (match) {
            case IMAGES_THUMBNAILS:
            case IMAGES_THUMBNAILS_ID:
            case VIDEO_THUMBNAILS:
            case VIDEO_THUMBNAILS_ID:
            case AUDIO_ALBUMART:
            case AUDIO_ALBUMART_ID:
                isThumbnail = true;
                break;
            default:
                isThumbnail = false;
                break;
        }

        // If we're touching columns that would change placement of a file,
        // blend in current values and recalculate path
        if (containsAny(initialValues.keySet(), sPlacementColumns)
                && !initialValues.containsKey(MediaColumns.DATA)
                && !isCallingPackageSystem()
                && !isThumbnail) {
            Trace.traceBegin(TRACE_TAG_DATABASE, "movement");

            // We only support movement under well-defined collections
            switch (match) {
                case AUDIO_MEDIA_ID:
                case VIDEO_MEDIA_ID:
                case IMAGES_MEDIA_ID:
                case DOWNLOADS_ID:
                    break;
                default:
                    throw new IllegalArgumentException("Movement of " + uri
                            + " which isn't part of well-defined collection not allowed");
            }

            final LocalCallingIdentity token = clearLocalCallingIdentity();
            try (Cursor c = queryForSingleItem(uri,
                    sPlacementColumns.toArray(EmptyArray.STRING), userWhere, userWhereArgs, null)) {
                for (int i = 0; i < c.getColumnCount(); i++) {
                    final String column = c.getColumnName(i);
                    if (!initialValues.containsKey(column)) {
                        initialValues.put(column, c.getString(i));
                    }
                }
            } catch (FileNotFoundException e) {
                throw new IllegalStateException(e);
            } finally {
                restoreLocalCallingIdentity(token);
            }

            // Regenerate path using blended values; this will throw if caller
            // is attempting to place file into invalid location
            final String beforePath = initialValues.getAsString(MediaColumns.DATA);
            final String beforeVolume = extractVolumeName(beforePath);
            final String beforeOwner = extractPathOwnerPackageName(beforePath);
            initialValues.remove(MediaColumns.DATA);
            try {
                ensureNonUniqueFileColumns(match, uri, initialValues, beforePath);
            } catch (VolumeArgumentException e) {
                return e.translateForUpdateDelete(targetSdkVersion);
            }

            final String probePath = initialValues.getAsString(MediaColumns.DATA);
            final String probeVolume = extractVolumeName(probePath);
            final String probeOwner = extractPathOwnerPackageName(probePath);
            if (Objects.equals(beforePath, probePath)) {
                Log.d(TAG, "Identical paths " + beforePath + "; not moving");
            } else if (!Objects.equals(beforeVolume, probeVolume)) {
                throw new IllegalArgumentException("Changing volume from " + beforePath + " to "
                        + probePath + " not allowed");
            } else if (!Objects.equals(beforeOwner, probeOwner)) {
                throw new IllegalArgumentException("Changing ownership from " + beforePath + " to "
                        + probePath + " not allowed");
            } else {
                // Now that we've confirmed an actual movement is taking place,
                // ensure we have a unique destination
                initialValues.remove(MediaColumns.DATA);
                try {
                    ensureUniqueFileColumns(match, uri, initialValues);
                } catch (VolumeArgumentException e) {
                    return e.translateForUpdateDelete(targetSdkVersion);
                }
                final String afterPath = initialValues.getAsString(MediaColumns.DATA);

                Log.d(TAG, "Moving " + beforePath + " to " + afterPath);
                try {
                    Os.rename(beforePath, afterPath);
                } catch (ErrnoException e) {
                    throw new IllegalStateException(e);
                }
                initialValues.put(MediaColumns.DATA, afterPath);
            }

            Trace.traceEnd(TRACE_TAG_DATABASE);
        }

        // Make sure any updated paths look sane
        try {
            assertFileColumnsSane(match, uri, initialValues);
        } catch (VolumeArgumentException e) {
            return e.translateForUpdateDelete(targetSdkVersion);
        }

        // if the media type is being changed, check if it's being changed from image or video
        // to something else
        if (initialValues.containsKey(FileColumns.MEDIA_TYPE)) {
            final int newMediaType = initialValues.getAsInteger(FileColumns.MEDIA_TYPE);

            // If we're changing media types, invalidate any cached "empty"
            // answers for the new collection type.
            MediaDocumentsProvider.onMediaStoreInsert(
                    getContext(), volumeName, newMediaType, -1);

            // If we're changing media types, invalidate any thumbnails
            triggerInvalidate = true;
        }

        if (initialValues.containsKey(FileColumns.DATA)) {
            // If we're changing paths, invalidate any thumbnails
            triggerInvalidate = true;
        }

        // Since the update mutation may prevent us from matching items after
        // it's applied, we need to snapshot affected IDs here
        final LongArray updatedIds = new LongArray();
        if (triggerInvalidate || triggerScan) {
            Trace.traceBegin(TRACE_TAG_DATABASE, "snapshot");
            final LocalCallingIdentity token = clearLocalCallingIdentity();
            try (Cursor c = qb.query(db, new String[] { FileColumns._ID },
                    userWhere, userWhereArgs, null, null, null)) {
                while (c.moveToNext()) {
                    updatedIds.add(c.getLong(0));
                }
            } finally {
                restoreLocalCallingIdentity(token);
                Trace.traceEnd(TRACE_TAG_DATABASE);
            }
        }

        // special case renaming directories via MTP.
        // in this case we must update all paths in the database with
        // the directory name as a prefix
        if ((match == MTP_OBJECTS || match == MTP_OBJECTS_ID || match == FILES_DIRECTORY)
                && initialValues != null
                // Is a rename operation
                && ((initialValues.size() == 1 && initialValues.containsKey(FileColumns.DATA))
                // Is a move operation
                || (initialValues.size() == 2 && initialValues.containsKey(FileColumns.DATA)
                && initialValues.containsKey(FileColumns.PARENT)))) {
            String oldPath = null;
            String newPath = initialValues.getAsString(MediaStore.MediaColumns.DATA);
            synchronized (mDirectoryCache) {
                mDirectoryCache.remove(newPath);
            }
            // MtpDatabase will rename the directory first, so we test the new file name
            File f = new File(newPath);
            if (newPath != null && f.isDirectory()) {
                Cursor cursor = qb.query(db, PATH_PROJECTION, userWhere, userWhereArgs, null, null,
                        null, null);
                try {
                    if (cursor != null && cursor.moveToNext()) {
                        oldPath = cursor.getString(1);
                    }
                } finally {
                    IoUtils.closeQuietly(cursor);
                }
                final boolean isDownload = isDownload(newPath);
                if (oldPath != null) {
                    synchronized (mDirectoryCache) {
                        mDirectoryCache.remove(oldPath);
                    }
                    final boolean wasDownload = isDownload(oldPath);
                    // first rename the row for the directory
                    count = qb.update(db, initialValues, userWhere, userWhereArgs);
                    if (count > 0) {
                        // update the paths of any files and folders contained in the directory
                        Object[] bindArgs = new Object[] {
                                newPath,
                                oldPath.length() + 1,
                                oldPath + "/",
                                oldPath + "0",
                                // update bucket_display_name and bucket_id based on new path
                                f.getName(),
                                f.toString().toLowerCase().hashCode(),
                                isDownload
                                };
                        db.execSQL("UPDATE files SET _data=?1||SUBSTR(_data, ?2)" +
                                // also update bucket_display_name
                                ",bucket_display_name=?5" +
                                ",bucket_id=?6" +
                                ",is_download=?7" +
                                " WHERE _data >= ?3 AND _data < ?4;",
                                bindArgs);
                    }

                    if (count > 0) {
                        acceptWithExpansion(helper::notifyChange, uri);
                    }
                    if (f.getName().startsWith(".")) {
                        MediaScanner.instance(getContext()).scanFile(new File(newPath));
                    }
                    return count;
                }
            } else if (newPath.toLowerCase(Locale.US).endsWith("/.nomedia")) {
                MediaScanner.instance(getContext()).scanFile(new File(newPath).getParentFile());
            }
        }

        switch (match) {
            case AUDIO_MEDIA:
            case AUDIO_MEDIA_ID:
                {
                    ContentValues values = new ContentValues(initialValues);
                    String albumartist = values.getAsString(MediaStore.Audio.Media.ALBUM_ARTIST);
                    String compilation = values.getAsString(MediaStore.Audio.Media.COMPILATION);
                    values.remove(MediaStore.Audio.Media.COMPILATION);

                    // Insert the artist into the artist table and remove it from
                    // the input values
                    String artist = values.getAsString("artist");
                    values.remove("artist");
                    if (artist != null) {
                        long artistRowId;
                        ArrayMap<String, Long> artistCache = helper.mArtistCache;
                        synchronized(artistCache) {
                            Long temp = artistCache.get(artist);
                            if (temp == null) {
                                artistRowId = getKeyIdForName(helper, db,
                                        "artists", "artist_key", "artist",
                                        artist, artist, null, 0, null, artistCache, uri);
                            } else {
                                artistRowId = temp.longValue();
                            }
                        }
                        values.put("artist_id", Integer.toString((int)artistRowId));
                    }

                    // Do the same for the album field.
                    String so = values.getAsString("album");
                    values.remove("album");
                    if (so != null) {
                        String path = values.getAsString(MediaStore.MediaColumns.DATA);
                        int albumHash = 0;
                        if (albumartist != null) {
                            albumHash = albumartist.hashCode();
                        } else if (compilation != null && compilation.equals("1")) {
                            // nothing to do, hash already set
                        } else {
                            if (path == null) {
                                if (match == AUDIO_MEDIA) {
                                    Log.w(TAG, "Possible multi row album name update without"
                                            + " path could give wrong album key");
                                } else {
                                    //Log.w(TAG, "Specify path to avoid extra query");
                                    Cursor c = query(uri,
                                            new String[] { MediaStore.Audio.Media.DATA},
                                            null, null, null);
                                    if (c != null) {
                                        try {
                                            int numrows = c.getCount();
                                            if (numrows == 1) {
                                                c.moveToFirst();
                                                path = c.getString(0);
                                            } else {
                                                Log.e(TAG, "" + numrows + " rows for " + uri);
                                            }
                                        } finally {
                                            IoUtils.closeQuietly(c);
                                        }
                                    }
                                }
                            }
                            if (path != null) {
                                albumHash = path.substring(0, path.lastIndexOf('/')).hashCode();
                            }
                        }

                        String s = so.toString();
                        long albumRowId;
                        ArrayMap<String, Long> albumCache = helper.mAlbumCache;
                        synchronized(albumCache) {
                            String cacheName = s + albumHash;
                            Long temp = albumCache.get(cacheName);
                            if (temp == null) {
                                albumRowId = getKeyIdForName(helper, db,
                                        "albums", "album_key", "album",
                                        s, cacheName, path, albumHash, artist, albumCache, uri);
                            } else {
                                albumRowId = temp.longValue();
                            }
                        }
                        values.put("album_id", Integer.toString((int)albumRowId));
                    }

                    // don't allow the title_key field to be updated directly
                    values.remove("title_key");
                    // If the title field is modified, update the title_key
                    so = values.getAsString("title");
                    if (so != null) {
                        try {
                            final String localizedTitle = getLocalizedTitle(so);
                            if (localizedTitle != null) {
                                values.put("title_resource_uri", so);
                                so = localizedTitle;
                            } else {
                                values.putNull("title_resource_uri");
                            }
                        } catch (Exception e) {
                            values.put("title_resource_uri", so);
                        }
                        values.put("title_key", MediaStore.Audio.keyFor(so));
                        // do a final trim of the title, in case it started with the special
                        // "sort first" character (ascii \001)
                        values.put("title", so.trim());
                    }

                    count = qb.update(db, values, userWhere, userWhereArgs);
                    if (genre != null) {
                        if (count == 1 && match == AUDIO_MEDIA_ID) {
                            long rowId = Long.parseLong(uri.getPathSegments().get(3));
                            updateGenre(rowId, genre, volumeName);
                        } else {
                            // can't handle genres for bulk update or for non-audio files
                            Log.w(TAG, "ignoring genre in update: count = "
                                    + count + " match = " + match);
                        }
                    }
                }
                break;
            case IMAGES_MEDIA:
            case IMAGES_MEDIA_ID:
            case VIDEO_MEDIA:
            case VIDEO_MEDIA_ID:
                {
                    ContentValues values = new ContentValues(initialValues);
                    // Don't allow bucket id or display name to be updated directly.
                    // The same names are used for both images and table columns, so
                    // we use the ImageColumns constants here.
                    values.remove(ImageColumns.BUCKET_ID);
                    values.remove(ImageColumns.BUCKET_DISPLAY_NAME);
                    // If the data is being modified update the bucket values
                    computeDataValues(values);
                    count = qb.update(db, values, userWhere, userWhereArgs);
                }
                break;

            case AUDIO_MEDIA_ID_PLAYLISTS_ID:
            case AUDIO_PLAYLISTS_ID:
                long playlistId = ContentUris.parseId(uri);
                count = qb.update(db, initialValues, userWhere, userWhereArgs);
                if (count > 0) {
                    updatePlaylistDateModifiedToNow(db, playlistId);
                }
                break;
            case AUDIO_PLAYLISTS_ID_MEMBERS:
                long playlistIdMembers = Long.parseLong(uri.getPathSegments().get(3));
                count = qb.update(db, initialValues, userWhere, userWhereArgs);
                if (count > 0) {
                    updatePlaylistDateModifiedToNow(db, playlistIdMembers);
                }
                break;
            case AUDIO_PLAYLISTS_ID_MEMBERS_ID:
                String moveit = uri.getQueryParameter("move");
                if (moveit != null) {
                    String key = MediaStore.Audio.Playlists.Members.PLAY_ORDER;
                    if (initialValues.containsKey(key)) {
                        int newpos = initialValues.getAsInteger(key);
                        List <String> segments = uri.getPathSegments();
                        long playlist = Long.parseLong(segments.get(3));
                        int oldpos = Integer.parseInt(segments.get(5));
                        int rowsChanged = movePlaylistEntry(volumeName, helper, db, playlist, oldpos, newpos);
                        if (rowsChanged > 0) {
                            updatePlaylistDateModifiedToNow(db, playlist);
                        }

                        return rowsChanged;
                    }
                    throw new IllegalArgumentException("Need to specify " + key +
                            " when using 'move' parameter");
                }
                // fall through
            default:
                count = qb.update(db, initialValues, userWhere, userWhereArgs);
                break;
        }

        // If the caller tried (and failed) to update metadata, the file on disk
        // might have changed, to scan it to collect the latest metadata.
        if (triggerInvalidate || triggerScan) {
            Trace.traceBegin(TRACE_TAG_DATABASE, "invalidate");
            final LocalCallingIdentity token = clearLocalCallingIdentity();
            try {
                for (int i = 0; i < updatedIds.size(); i++) {
                    final long updatedId = updatedIds.get(i);
                    final Uri updatedUri = Files.getContentUri(volumeName, updatedId);
                    BackgroundThread.getExecutor().execute(() -> {
                        invalidateThumbnails(updatedUri);
                    });

                    if (triggerScan) {
                        try (Cursor c = queryForSingleItem(updatedUri,
                                new String[] { FileColumns.DATA }, null, null, null)) {
                            MediaScanner.instance(getContext()).scanFile(new File(c.getString(0)));
                        } catch (Exception e) {
                            Log.w(TAG, "Failed to update metadata for " + updatedUri, e);
                        }
                    }
                }
            } finally {
                restoreLocalCallingIdentity(token);
                Trace.traceEnd(TRACE_TAG_DATABASE);
            }
        }

        if (count > 0) {
            acceptWithExpansion(helper::notifyChange, uri);
        }
        return count;
    }

    private int movePlaylistEntry(String volumeName, DatabaseHelper helper, SQLiteDatabase db,
            long playlist, int from, int to) {
        if (from == to) {
            return 0;
        }
        db.beginTransaction();
        int numlines = 0;
        Cursor c = null;
        try {
            c = db.query("audio_playlists_map",
                    new String [] {"play_order" },
                    "playlist_id=?", new String[] {"" + playlist}, null, null, "play_order",
                    from + ",1");
            c.moveToFirst();
            int from_play_order = c.getInt(0);
            IoUtils.closeQuietly(c);
            c = db.query("audio_playlists_map",
                    new String [] {"play_order" },
                    "playlist_id=?", new String[] {"" + playlist}, null, null, "play_order",
                    to + ",1");
            c.moveToFirst();
            int to_play_order = c.getInt(0);
            db.execSQL("UPDATE audio_playlists_map SET play_order=-1" +
                    " WHERE play_order=" + from_play_order +
                    " AND playlist_id=" + playlist);
            // We could just run both of the next two statements, but only one of
            // of them will actually do anything, so might as well skip the compile
            // and execute steps.
            if (from  < to) {
                db.execSQL("UPDATE audio_playlists_map SET play_order=play_order-1" +
                        " WHERE play_order<=" + to_play_order +
                        " AND play_order>" + from_play_order +
                        " AND playlist_id=" + playlist);
                numlines = to - from + 1;
            } else {
                db.execSQL("UPDATE audio_playlists_map SET play_order=play_order+1" +
                        " WHERE play_order>=" + to_play_order +
                        " AND play_order<" + from_play_order +
                        " AND playlist_id=" + playlist);
                numlines = from - to + 1;
            }
            db.execSQL("UPDATE audio_playlists_map SET play_order=" + to_play_order +
                    " WHERE play_order=-1 AND playlist_id=" + playlist);
            db.setTransactionSuccessful();
        } finally {
            db.endTransaction();
            IoUtils.closeQuietly(c);
        }

        Uri uri = ContentUris.withAppendedId(
                MediaStore.Audio.Playlists.getContentUri(volumeName), playlist);
        // notifyChange() must be called after the database transaction is ended
        // or the listeners will read the old data in the callback
        getContext().getContentResolver().notifyChange(uri, null);

        return numlines;
    }

    private void updatePlaylistDateModifiedToNow(SQLiteDatabase database, long playlistId) {
        ContentValues values = new ContentValues();
        values.put(
                FileColumns.DATE_MODIFIED,
                TimeUnit.MILLISECONDS.toSeconds(System.currentTimeMillis())
        );

        database.update(
                MediaStore.Files.TABLE,
                values,
                MediaStore.Files.FileColumns._ID + "=?",
                new String[]{String.valueOf(playlistId)}
        );
    }

    @Override
    public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException {
        return openFileCommon(uri, mode, null);
    }

    @Override
    public ParcelFileDescriptor openFile(Uri uri, String mode, CancellationSignal signal)
            throws FileNotFoundException {
        return openFileCommon(uri, mode, signal);
    }

    private ParcelFileDescriptor openFileCommon(Uri uri, String mode, CancellationSignal signal)
            throws FileNotFoundException {
        uri = safeUncanonicalize(uri);

        final boolean allowHidden = isCallingPackageAllowedHidden();
        final int match = matchUri(uri, allowHidden);
        final String volumeName = getVolumeName(uri);

        // Handle some legacy cases where we need to redirect thumbnails
        switch (match) {
            case AUDIO_ALBUMART_ID: {
                final long albumId = Long.parseLong(uri.getPathSegments().get(3));
                final Uri targetUri = ContentUris
                        .withAppendedId(Audio.Albums.getContentUri(volumeName), albumId);
                return ParcelFileDescriptor.open(ensureThumbnail(targetUri, signal),
                        ParcelFileDescriptor.MODE_READ_ONLY);

            }
            case AUDIO_ALBUMART_FILE_ID: {
                final long audioId = Long.parseLong(uri.getPathSegments().get(3));
                final Uri targetUri = ContentUris
                        .withAppendedId(Audio.Media.getContentUri(volumeName), audioId);
                return ParcelFileDescriptor.open(ensureThumbnail(targetUri, signal),
                        ParcelFileDescriptor.MODE_READ_ONLY);
            }
            case VIDEO_MEDIA_ID_THUMBNAIL: {
                final long videoId = Long.parseLong(uri.getPathSegments().get(3));
                final Uri targetUri = ContentUris
                        .withAppendedId(Video.Media.getContentUri(volumeName), videoId);
                return ParcelFileDescriptor.open(ensureThumbnail(targetUri, signal),
                        ParcelFileDescriptor.MODE_READ_ONLY);
            }
            case IMAGES_MEDIA_ID_THUMBNAIL: {
                final long imageId = Long.parseLong(uri.getPathSegments().get(3));
                final Uri targetUri = ContentUris
                        .withAppendedId(Images.Media.getContentUri(volumeName), imageId);
                return ParcelFileDescriptor.open(ensureThumbnail(targetUri, signal),
                        ParcelFileDescriptor.MODE_READ_ONLY);
            }
        }

        return openFileAndEnforcePathPermissionsHelper(uri, match, mode, signal);
    }

    @Override
    public AssetFileDescriptor openTypedAssetFile(Uri uri, String mimeTypeFilter, Bundle opts)
            throws FileNotFoundException {
        return openTypedAssetFileCommon(uri, mimeTypeFilter, opts, null);
    }

    @Override
    public AssetFileDescriptor openTypedAssetFile(Uri uri, String mimeTypeFilter, Bundle opts,
            CancellationSignal signal) throws FileNotFoundException {
        return openTypedAssetFileCommon(uri, mimeTypeFilter, opts, signal);
    }

    private AssetFileDescriptor openTypedAssetFileCommon(Uri uri, String mimeTypeFilter,
            Bundle opts, CancellationSignal signal) throws FileNotFoundException {
        uri = safeUncanonicalize(uri);

        // TODO: enforce that caller has access to this uri

        // Offer thumbnail of media, when requested
        final boolean wantsThumb = (opts != null) && opts.containsKey(ContentResolver.EXTRA_SIZE)
                && (mimeTypeFilter != null) && mimeTypeFilter.startsWith("image/");
        if (wantsThumb) {
            final File thumbFile = ensureThumbnail(uri, signal);
            return new AssetFileDescriptor(
                    ParcelFileDescriptor.open(thumbFile, ParcelFileDescriptor.MODE_READ_ONLY),
                    0, AssetFileDescriptor.UNKNOWN_LENGTH);
        }

        // Worst case, return the underlying file
        return new AssetFileDescriptor(openFileCommon(uri, "r", signal), 0,
                AssetFileDescriptor.UNKNOWN_LENGTH);
    }

    private File ensureThumbnail(Uri uri, CancellationSignal signal) throws FileNotFoundException {
        final boolean allowHidden = isCallingPackageAllowedHidden();
        final int match = matchUri(uri, allowHidden);

        Trace.traceBegin(TRACE_TAG_DATABASE, "ensureThumbnail");
        final LocalCallingIdentity token = clearLocalCallingIdentity();
        try {
            final File thumbFile;
            switch (match) {
                case AUDIO_ALBUMS_ID: {
                    final String volumeName = MediaStore.getVolumeName(uri);
                    final Uri baseUri = MediaStore.Audio.Media.getContentUri(volumeName);
                    final long albumId = ContentUris.parseId(uri);
                    try (Cursor c = query(baseUri, new String[] { MediaStore.Audio.Media._ID },
                            MediaStore.Audio.Media.ALBUM_ID + "=" + albumId, null, null, signal)) {
                        if (c.moveToFirst()) {
                            final long audioId = c.getLong(0);
                            final Uri targetUri = ContentUris.withAppendedId(baseUri, audioId);
                            return mAudioThumbnailer.ensureThumbnail(targetUri, signal);
                        } else {
                            throw new FileNotFoundException("No media for album " + uri);
                        }
                    }
                }
                case AUDIO_MEDIA_ID:
                    return mAudioThumbnailer.ensureThumbnail(uri, signal);
                case VIDEO_MEDIA_ID:
                    return mVideoThumbnailer.ensureThumbnail(uri, signal);
                case IMAGES_MEDIA_ID:
                    return mImageThumbnailer.ensureThumbnail(uri, signal);
                default:
                    throw new FileNotFoundException();
            }
        } catch (IOException e) {
            Log.w(TAG, e);
            throw new FileNotFoundException(e.getMessage());
        } finally {
            restoreLocalCallingIdentity(token);
            Trace.traceEnd(TRACE_TAG_DATABASE);
        }
    }

    /**
     * Update the metadata columns for the image residing at given {@link Uri}
     * by reading data from the underlying image.
     */
    private void updateImageMetadata(ContentValues values, File file) {
        final BitmapFactory.Options bitmapOpts = new BitmapFactory.Options();
        bitmapOpts.inJustDecodeBounds = true;
        BitmapFactory.decodeFile(file.getAbsolutePath(), bitmapOpts);

        values.put(MediaColumns.WIDTH, bitmapOpts.outWidth);
        values.put(MediaColumns.HEIGHT, bitmapOpts.outHeight);
    }

    /**
     * Return the {@link MediaColumns#DATA} field for the given {@code Uri}.
     */
    File queryForDataFile(Uri uri, CancellationSignal signal)
            throws FileNotFoundException {
        return queryForDataFile(uri, null, null, signal);
    }

    /**
     * Return the {@link MediaColumns#DATA} field for the given {@code Uri}.
     */
    File queryForDataFile(Uri uri, String selection, String[] selectionArgs,
            CancellationSignal signal) throws FileNotFoundException {
        try (Cursor cursor = queryForSingleItem(uri, new String[] { MediaColumns.DATA },
                selection, selectionArgs, signal)) {
            final String data = cursor.getString(0);
            if (TextUtils.isEmpty(data)) {
                throw new FileNotFoundException("Missing path for " + uri);
            } else {
                return new File(data);
            }
        }
    }

    /**
     * Return the {@link Uri} for the given {@code File}.
     */
    Uri queryForMediaUri(File file, CancellationSignal signal) throws FileNotFoundException {
        final String volumeName = MediaStore.getVolumeName(file);
        final Uri uri = Files.getContentUri(volumeName);
        try (Cursor cursor = queryForSingleItem(uri, new String[] { MediaColumns._ID },
                MediaColumns.DATA + "=?", new String[] { file.getAbsolutePath() }, signal)) {
            return ContentUris.withAppendedId(uri, cursor.getLong(0));
        }
    }

    /**
     * Query the given {@link Uri}, expecting only a single item to be found.
     *
     * @throws FileNotFoundException if no items were found, or multiple items
     *             were found, or there was trouble reading the data.
     */
    Cursor queryForSingleItem(Uri uri, String[] projection, String selection,
            String[] selectionArgs, CancellationSignal signal) throws FileNotFoundException {
        final Cursor c = query(uri, projection,
                ContentResolver.createSqlQueryBundle(selection, selectionArgs, null), signal);
        if (c == null) {
            throw new FileNotFoundException("Missing cursor for " + uri);
        } else if (c.getCount() < 1) {
            IoUtils.closeQuietly(c);
            throw new FileNotFoundException("No item at " + uri);
        } else if (c.getCount() > 1) {
            IoUtils.closeQuietly(c);
            throw new FileNotFoundException("Multiple items at " + uri);
        }

        if (c.moveToFirst()) {
            return c;
        } else {
            IoUtils.closeQuietly(c);
            throw new FileNotFoundException("Failed to read row from " + uri);
        }
    }

    /**
     * Replacement for {@link #openFileHelper(Uri, String)} which enforces any
     * permissions applicable to the path before returning.
     */
    private ParcelFileDescriptor openFileAndEnforcePathPermissionsHelper(Uri uri, int match,
            String mode, CancellationSignal signal) throws FileNotFoundException {
        final int modeBits = ParcelFileDescriptor.parseMode(mode);
        final boolean forWrite = (modeBits != ParcelFileDescriptor.MODE_READ_ONLY);

        final boolean hasOwnerPackageName = hasOwnerPackageName(uri);
        final String[] projection = new String[] {
                MediaColumns.DATA,
                hasOwnerPackageName ? MediaColumns.OWNER_PACKAGE_NAME : "NULL",
                hasOwnerPackageName ? MediaColumns.IS_PENDING : "0",
        };

        final File file;
        final String ownerPackageName;
        final boolean isPending;
        final LocalCallingIdentity token = clearLocalCallingIdentity();
        try (Cursor c = queryForSingleItem(uri, projection, null, null, signal)) {
            final String data = c.getString(0);
            if (TextUtils.isEmpty(data)) {
                throw new FileNotFoundException("Missing path for " + uri);
            } else {
                file = new File(data).getCanonicalFile();
            }
            ownerPackageName = c.getString(1);
            isPending = c.getInt(2) != 0;
        } catch (IOException e) {
            throw new FileNotFoundException(e.toString());
        } finally {
            restoreLocalCallingIdentity(token);
        }

        checkAccess(uri, file, forWrite);

        // Require ownership if item is still pending
        final boolean hasOwner = (ownerPackageName != null);
        final boolean callerIsOwner = Objects.equals(getCallingPackageOrSelf(), ownerPackageName);
        if (isPending && hasOwner && !callerIsOwner) {
            throw new IllegalStateException(
                    "Only owner is able to interact with pending media " + uri);
        }

        // Figure out if we need to redact contents
        final boolean redactionNeeded = callerIsOwner ? false : isRedactionNeeded(uri);
        final RedactionInfo redactionInfo = redactionNeeded ? getRedactionRanges(file)
                : new RedactionInfo(EmptyArray.LONG, EmptyArray.LONG);

        // Yell if caller requires original, since we can't give it to them
        // unless they have access granted above
        if (redactionNeeded
                && parseBoolean(uri.getQueryParameter(MediaStore.PARAM_REQUIRE_ORIGINAL))) {
            throw new UnsupportedOperationException(
                    "Caller must hold ACCESS_MEDIA_LOCATION permission to access original");
        }

        // Kick off metadata update when writing is finished
        final OnCloseListener listener = (e) -> {
            // We always update metadata to reflect the state on disk, even when
            // the remote writer tried claiming an exception
            invalidateThumbnails(uri);

            try {
                switch (match) {
                    case IMAGES_THUMBNAILS_ID:
                    case VIDEO_THUMBNAILS_ID:
                        final ContentValues values = new ContentValues();
                        updateImageMetadata(values, file);
                        update(uri, values, null, null);
                        break;
                    default:
                        MediaScanner.instance(getContext()).scanFile(file);
                        break;
                }
            } catch (Exception e2) {
                Log.w(TAG, "Failed to update metadata for " + uri, e2);
            }
        };

        try {
            // First, handle any redaction that is needed for caller
            final ParcelFileDescriptor pfd;
            if (redactionInfo.redactionRanges.length > 0) {
                pfd = RedactingFileDescriptor.open(
                        getContext(),
                        file,
                        modeBits,
                        redactionInfo.redactionRanges,
                        redactionInfo.freeOffsets);
            } else {
                pfd = ParcelFileDescriptor.open(file, modeBits);
            }

            // Second, wrap in any listener that we've requested
            if (!isPending && forWrite && listener != null) {
                return ParcelFileDescriptor.fromPfd(pfd, BackgroundThread.getHandler(), listener);
            } else {
                return pfd;
            }
        } catch (IOException e) {
            if (e instanceof FileNotFoundException) {
                throw (FileNotFoundException) e;
            } else {
                throw new IllegalStateException(e);
            }
        }
    }

    private void deleteIfAllowed(Uri uri, String path) {
        try {
            final File file = new File(path);
            checkAccess(uri, file, true);
            file.delete();
        } catch (Exception e) {
            Log.e(TAG, "Couldn't delete " + path, e);
        }
    }

    @Deprecated
    private boolean isPending(Uri uri) {
        final int match = matchUri(uri, true);
        switch (match) {
            case AUDIO_MEDIA_ID:
            case VIDEO_MEDIA_ID:
            case IMAGES_MEDIA_ID:
                try (Cursor c = queryForSingleItem(uri,
                        new String[] { MediaColumns.IS_PENDING }, null, null, null)) {
                    return (c.getInt(0) != 0);
                } catch (FileNotFoundException e) {
                    throw new IllegalStateException(e);
                }
            default:
                return false;
        }
    }

    @Deprecated
    private boolean isRedactionNeeded(Uri uri) {
        return mCallingIdentity.get().hasPermission(PERMISSION_IS_REDACTION_NEEDED);
    }

    /**
     * Set of Exif tags that should be considered for redaction.
     */
    private static final String[] REDACTED_EXIF_TAGS = new String[] {
            ExifInterface.TAG_GPS_ALTITUDE,
            ExifInterface.TAG_GPS_ALTITUDE_REF,
            ExifInterface.TAG_GPS_AREA_INFORMATION,
            ExifInterface.TAG_GPS_DOP,
            ExifInterface.TAG_GPS_DATESTAMP,
            ExifInterface.TAG_GPS_DEST_BEARING,
            ExifInterface.TAG_GPS_DEST_BEARING_REF,
            ExifInterface.TAG_GPS_DEST_DISTANCE,
            ExifInterface.TAG_GPS_DEST_DISTANCE_REF,
            ExifInterface.TAG_GPS_DEST_LATITUDE,
            ExifInterface.TAG_GPS_DEST_LATITUDE_REF,
            ExifInterface.TAG_GPS_DEST_LONGITUDE,
            ExifInterface.TAG_GPS_DEST_LONGITUDE_REF,
            ExifInterface.TAG_GPS_DIFFERENTIAL,
            ExifInterface.TAG_GPS_IMG_DIRECTION,
            ExifInterface.TAG_GPS_IMG_DIRECTION_REF,
            ExifInterface.TAG_GPS_LATITUDE,
            ExifInterface.TAG_GPS_LATITUDE_REF,
            ExifInterface.TAG_GPS_LONGITUDE,
            ExifInterface.TAG_GPS_LONGITUDE_REF,
            ExifInterface.TAG_GPS_MAP_DATUM,
            ExifInterface.TAG_GPS_MEASURE_MODE,
            ExifInterface.TAG_GPS_PROCESSING_METHOD,
            ExifInterface.TAG_GPS_SATELLITES,
            ExifInterface.TAG_GPS_SPEED,
            ExifInterface.TAG_GPS_SPEED_REF,
            ExifInterface.TAG_GPS_STATUS,
            ExifInterface.TAG_GPS_TIMESTAMP,
            ExifInterface.TAG_GPS_TRACK,
            ExifInterface.TAG_GPS_TRACK_REF,
            ExifInterface.TAG_GPS_VERSION_ID,
    };

    /**
     * Set of ISO boxes that should be considered for redaction.
     */
    private static final int[] REDACTED_ISO_BOXES = new int[] {
            IsoInterface.BOX_LOCI,
            IsoInterface.BOX_XYZ,
            IsoInterface.BOX_GPS,
            IsoInterface.BOX_GPS0,
    };

    private static final class RedactionInfo {
        public final long[] redactionRanges;
        public final long[] freeOffsets;
        public RedactionInfo(long[] redactionRanges, long[] freeOffsets) {
            this.redactionRanges = redactionRanges;
            this.freeOffsets = freeOffsets;
        }
    }

    private RedactionInfo getRedactionRanges(File file) {
        Trace.traceBegin(TRACE_TAG_DATABASE, "getRedactionRanges");
        final LongArray res = new LongArray();
        final LongArray freeOffsets = new LongArray();
        try (FileInputStream is = new FileInputStream(file)) {
            final ExifInterface exif = new ExifInterface(is.getFD());
            for (String tag : REDACTED_EXIF_TAGS) {
                final long[] range = exif.getAttributeRange(tag);
                if (range != null) {
                    res.add(range[0]);
                    res.add(range[0] + range[1]);
                }
            }

            final IsoInterface iso = IsoInterface.fromFileDescriptor(is.getFD());
            for (int box : REDACTED_ISO_BOXES) {
                final long[] ranges = iso.getBoxRanges(box);
                for (int i = 0; i < ranges.length; i += 2) {
                    long boxTypeOffset = ranges[i] - 4;
                    freeOffsets.add(boxTypeOffset);
                    res.add(boxTypeOffset);
                    res.add(ranges[i + 1]);
                }
            }

            // Redact xmp where present
            final Set<String> redactedXmpTags = new ArraySet<>(Arrays.asList(REDACTED_EXIF_TAGS));
            final XmpInterface exifXmp = XmpInterface.fromContainer(exif, redactedXmpTags);
            res.addAll(exifXmp.getRedactionRanges());
            final XmpInterface isoXmp = XmpInterface.fromContainer(iso, redactedXmpTags);
            res.addAll(isoXmp.getRedactionRanges());
        } catch (IOException e) {
            Log.w(TAG, "Failed to redact " + file + ": " + e);
        }
        Trace.traceEnd(TRACE_TAG_DATABASE);
        return new RedactionInfo(res.toArray(), freeOffsets.toArray());
    }

    private boolean checkCallingPermissionGlobal(Uri uri, boolean forWrite) {
        // System internals can work with all media
        if (isCallingPackageSystem()) {
            return true;
        }

        // Check if caller is known to be owner of this item, to speed up
        // performance of our permission checks
        final int table = matchUri(uri, true);
        switch (table) {
            case AUDIO_MEDIA_ID:
            case VIDEO_MEDIA_ID:
            case IMAGES_MEDIA_ID:
            case FILES_ID:
            case DOWNLOADS_ID:
                final long id = ContentUris.parseId(uri);
                if (mCallingIdentity.get().isOwned(id)) {
                    return true;
                }
        }

        // Outstanding grant means they get access
        if (getContext().checkUriPermission(uri, mCallingIdentity.get().pid,
                mCallingIdentity.get().uid, forWrite
                        ? Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                        : Intent.FLAG_GRANT_READ_URI_PERMISSION) == PERMISSION_GRANTED) {
            return true;
        }

        return false;
    }

    private boolean checkCallingPermissionLegacy(Uri uri, boolean forWrite, String callingPackage) {
        return mCallingIdentity.get().hasPermission(PERMISSION_IS_LEGACY);
    }

    @Deprecated
    private boolean checkCallingPermissionAudio(boolean forWrite, String callingPackage) {
        if (forWrite) {
            return mCallingIdentity.get().hasPermission(PERMISSION_WRITE_AUDIO);
        } else {
            return mCallingIdentity.get().hasPermission(PERMISSION_READ_AUDIO);
        }
    }

    @Deprecated
    private boolean checkCallingPermissionVideo(boolean forWrite, String callingPackage) {
        if (forWrite) {
            return mCallingIdentity.get().hasPermission(PERMISSION_WRITE_VIDEO);
        } else {
            return mCallingIdentity.get().hasPermission(PERMISSION_READ_VIDEO);
        }
    }

    @Deprecated
    private boolean checkCallingPermissionImages(boolean forWrite, String callingPackage) {
        if (forWrite) {
            return mCallingIdentity.get().hasPermission(PERMISSION_WRITE_IMAGES);
        } else {
            return mCallingIdentity.get().hasPermission(PERMISSION_READ_IMAGES);
        }
    }

    /**
     * Enforce that caller has access to the given {@link Uri}.
     *
     * @throws SecurityException if access isn't allowed.
     */
    private void enforceCallingPermission(Uri uri, boolean forWrite) {
        Trace.traceBegin(TRACE_TAG_DATABASE, "enforceCallingPermission");
        try {
            enforceCallingPermissionInternal(uri, forWrite);
        } finally {
            Trace.traceEnd(TRACE_TAG_DATABASE);
        }
    }

    private void enforceCallingPermissionInternal(Uri uri, boolean forWrite) {
        // Try a simple global check first before falling back to performing a
        // simple query to probe for access.
        if (checkCallingPermissionGlobal(uri, forWrite)) {
            // Access allowed, yay!
            return;
        }

        final DatabaseHelper helper;
        final SQLiteDatabase db;
        try {
            helper = getDatabaseForUri(uri);
            db = helper.getReadableDatabase();
        } catch (VolumeNotFoundException e) {
            throw e.rethrowAsIllegalArgumentException();
        }

        final boolean allowHidden = isCallingPackageAllowedHidden();
        final int table = matchUri(uri, allowHidden);

        // First, check to see if caller has direct write access
        if (forWrite) {
            final SQLiteQueryBuilder qb = getQueryBuilder(TYPE_UPDATE, uri, table, null);
            try (Cursor c = qb.query(db, new String[0], null, null, null, null, null)) {
                if (c.moveToFirst()) {
                    // Direct write access granted, yay!
                    return;
                }
            }
        }

        // We only allow the user to grant access to specific media items in
        // strongly typed collections; never to broad collections
        boolean allowUserGrant = false;
        final int matchUri = matchUri(uri, true);
        switch (matchUri) {
            case IMAGES_MEDIA_ID:
            case AUDIO_MEDIA_ID:
            case VIDEO_MEDIA_ID:
                allowUserGrant = true;
                break;
        }

        // Second, check to see if caller has direct read access
        final SQLiteQueryBuilder qb = getQueryBuilder(TYPE_QUERY, uri, table, null);
        try (Cursor c = qb.query(db, new String[0], null, null, null, null, null)) {
            if (c.moveToFirst()) {
                if (!forWrite) {
                    // Direct read access granted, yay!
                    return;
                } else if (allowUserGrant) {
                    // Caller has read access, but they wanted to write, and
                    // they'll need to get the user to grant that access
                    final Context context = getContext();
                    final PendingIntent intent = PendingIntent.getActivity(context, 42,
                            new Intent(null, uri, context, PermissionActivity.class),
                            FLAG_ONE_SHOT | FLAG_CANCEL_CURRENT | FLAG_IMMUTABLE);

                    final Icon icon = getCollectionIcon(uri);
                    final RemoteAction action = new RemoteAction(icon,
                            context.getText(R.string.permission_required_action),
                            context.getText(R.string.permission_required_action),
                            intent);

                    throw new RecoverableSecurityException(new SecurityException(
                            getCallingPackageOrSelf() + " has no access to " + uri),
                            context.getText(R.string.permission_required), action);
                }
            }
        }

        throw new SecurityException(getCallingPackageOrSelf() + " has no access to " + uri);
    }

    private Icon getCollectionIcon(Uri uri) {
        final PackageManager pm = getContext().getPackageManager();
        final String type = uri.getPathSegments().get(1);
        final String groupName;
        switch (type) {
            default: groupName = android.Manifest.permission_group.STORAGE; break;
        }
        try {
            final PermissionGroupInfo perm = pm.getPermissionGroupInfo(groupName, 0);
            return Icon.createWithResource(perm.packageName, perm.icon);
        } catch (NameNotFoundException e) {
            throw new RuntimeException(e);
        }
    }

    private void checkAccess(Uri uri, File file, boolean isWrite) throws FileNotFoundException {
        // First, does caller have the needed row-level access?
        enforceCallingPermission(uri, isWrite);

        // Second, does the path look sane?
        if (!FileUtils.contains(Environment.getStorageDirectory(), file)) {
            checkWorldReadAccess(file.getAbsolutePath());
        }
    }

    /**
     * Check whether the path is a world-readable file
     */
    private static void checkWorldReadAccess(String path) throws FileNotFoundException {
        // Path has already been canonicalized, and we relax the check to look
        // at groups to support runtime storage permissions.
        final int accessBits = path.startsWith("/storage/") ? OsConstants.S_IRGRP
                : OsConstants.S_IROTH;
        try {
            StructStat stat = Os.stat(path);
            if (OsConstants.S_ISREG(stat.st_mode) &&
                ((stat.st_mode & accessBits) == accessBits)) {
                checkLeadingPathComponentsWorldExecutable(path);
                return;
            }
        } catch (ErrnoException e) {
            // couldn't stat the file, either it doesn't exist or isn't
            // accessible to us
        }

        throw new FileNotFoundException("Can't access " + path);
    }

    private static void checkLeadingPathComponentsWorldExecutable(String filePath)
            throws FileNotFoundException {
        File parent = new File(filePath).getParentFile();

        // Path has already been canonicalized, and we relax the check to look
        // at groups to support runtime storage permissions.
        final int accessBits = filePath.startsWith("/storage/") ? OsConstants.S_IXGRP
                : OsConstants.S_IXOTH;

        while (parent != null) {
            if (! parent.exists()) {
                // parent dir doesn't exist, give up
                throw new FileNotFoundException("access denied");
            }
            try {
                StructStat stat = Os.stat(parent.getPath());
                if ((stat.st_mode & accessBits) != accessBits) {
                    // the parent dir doesn't have the appropriate access
                    throw new FileNotFoundException("Can't access " + filePath);
                }
            } catch (ErrnoException e1) {
                // couldn't stat() parent
                throw new FileNotFoundException("Can't access " + filePath);
            }
            parent = parent.getParentFile();
        }
    }

    /**
     * Look up the artist or album entry for the given name, creating that entry
     * if it does not already exists.
     * @param db        The database
     * @param table     The table to store the key/name pair in.
     * @param keyField  The name of the key-column
     * @param nameField The name of the name-column
     * @param rawName   The name that the calling app was trying to insert into the database
     * @param cacheName The string that will be inserted in to the cache
     * @param path      The full path to the file being inserted in to the audio table
     * @param albumHash A hash to distinguish between different albums of the same name
     * @param artist    The name of the artist, if known
     * @param cache     The cache to add this entry to
     * @param srcuri    The Uri that prompted the call to this method, used for determining whether this is
     *                  the internal or external database
     * @return          The row ID for this artist/album, or -1 if the provided name was invalid
     */
    private long getKeyIdForName(DatabaseHelper helper, SQLiteDatabase db,
            String table, String keyField, String nameField,
            String rawName, String cacheName, String path, int albumHash,
            String artist, ArrayMap<String, Long> cache, Uri srcuri) {
        long rowId;

        if (rawName == null || rawName.length() == 0) {
            rawName = MediaStore.UNKNOWN_STRING;
        }
        String k = MediaStore.Audio.keyFor(rawName);

        if (k == null) {
            // shouldn't happen, since we only get null keys for null inputs
            Log.e(TAG, "null key", new Exception());
            return -1;
        }

        boolean isAlbum = table.equals("albums");
        boolean isUnknown = MediaStore.UNKNOWN_STRING.equals(rawName);

        // To distinguish same-named albums, we append a hash. The hash is based
        // on the "album artist" tag if present, otherwise on the "compilation" tag
        // if present, otherwise on the path.
        // Ideally we would also take things like CDDB ID in to account, so
        // we can group files from the same album that aren't in the same
        // folder, but this is a quick and easy start that works immediately
        // without requiring support from the mp3, mp4 and Ogg meta data
        // readers, as long as the albums are in different folders.
        if (isAlbum) {
            k = k + albumHash;
            if (isUnknown) {
                k = k + artist;
            }
        }

        String [] selargs = { k };
        Cursor c = db.query(table, null, keyField + "=?", selargs, null, null, null);

        try {
            switch (c.getCount()) {
                case 0: {
                        // insert new entry into table
                        ContentValues otherValues = new ContentValues();
                        otherValues.put(keyField, k);
                        otherValues.put(nameField, rawName);
                        rowId = db.insert(table, "duration", otherValues);
                        if (rowId > 0) {
                            String volume = srcuri.toString().substring(16, 24); // extract internal/external
                            Uri uri = Uri.parse("content://media/" + volume + "/audio/" + table + "/" + rowId);
                            getContext().getContentResolver().notifyChange(uri, null);
                        }
                    }
                    break;
                case 1: {
                        // Use the existing entry
                        c.moveToFirst();
                        rowId = c.getLong(0);

                        // Determine whether the current rawName is better than what's
                        // currently stored in the table, and update the table if it is.
                        String currentFancyName = c.getString(2);
                        String bestName = makeBestName(rawName, currentFancyName);
                        if (!bestName.equals(currentFancyName)) {
                            // update the table with the new name
                            ContentValues newValues = new ContentValues();
                            newValues.put(nameField, bestName);
                            db.update(table, newValues, "rowid="+Integer.toString((int)rowId), null);
                            String volume = srcuri.toString().substring(16, 24); // extract internal/external
                            Uri uri = Uri.parse("content://media/" + volume + "/audio/" + table + "/" + rowId);
                            getContext().getContentResolver().notifyChange(uri, null);
                            // We have to remove the previous key from the cache otherwise we will
                            // not be able to change between upper and lower case letters.
                            if (isAlbum) {
                                cache.remove(currentFancyName + albumHash);
                            } else {
                                cache.remove(currentFancyName);
                            }
                        }
                    }
                    break;
                default:
                    // corrupt database
                    Log.e(TAG, "Multiple entries in table " + table + " for key " + k);
                    rowId = -1;
                    break;
            }
        } finally {
            IoUtils.closeQuietly(c);
        }

        if (cache != null && ! isUnknown) {
            cache.put(cacheName, rowId);
        }
        return rowId;
    }

    /**
     * Returns the best string to use for display, given two names.
     * Note that this function does not necessarily return either one
     * of the provided names; it may decide to return a better alternative
     * (for example, specifying the inputs "Police" and "Police, The" will
     * return "The Police")
     *
     * The basic assumptions are:
     * - longer is better ("The police" is better than "Police")
     * - prefix is better ("The Police" is better than "Police, The")
     * - accents are better ("Mot&ouml;rhead" is better than "Motorhead")
     *
     * @param one The first of the two names to consider
     * @param two The last of the two names to consider
     * @return The actual name to use
     */
    String makeBestName(String one, String two) {
        String name;

        // Longer names are usually better.
        if (one.length() > two.length()) {
            name = one;
        } else {
            // Names with accents are usually better, and conveniently sort later
            if (one.toLowerCase().compareTo(two.toLowerCase()) >= 0) {
                name = one;
            } else {
                name = two;
            }
        }

        // Prefixes are better than postfixes.
        if (name.endsWith(", the") || name.endsWith(",the") ||
            name.endsWith(", an") || name.endsWith(",an") ||
            name.endsWith(", a") || name.endsWith(",a")) {
            String fix = name.substring(1 + name.lastIndexOf(','));
            name = fix.trim() + " " + name.substring(0, name.lastIndexOf(','));
        }

        // TODO: word-capitalize the resulting name
        return name;
    }

    private static class FallbackException extends Exception {
        public FallbackException(String message) {
            super(message);
        }

        public IllegalArgumentException rethrowAsIllegalArgumentException() {
            throw new IllegalArgumentException(getMessage());
        }

        public Cursor translateForQuery(int targetSdkVersion) {
            if (targetSdkVersion >= Build.VERSION_CODES.Q) {
                throw new IllegalArgumentException(getMessage());
            } else {
                Log.w(TAG, getMessage());
                return null;
            }
        }

        public Uri translateForInsert(int targetSdkVersion) {
            if (targetSdkVersion >= Build.VERSION_CODES.Q) {
                throw new IllegalArgumentException(getMessage());
            } else {
                Log.w(TAG, getMessage());
                return null;
            }
        }

        public int translateForUpdateDelete(int targetSdkVersion) {
            if (targetSdkVersion >= Build.VERSION_CODES.Q) {
                throw new IllegalArgumentException(getMessage());
            } else {
                Log.w(TAG, getMessage());
                return 0;
            }
        }
    }

    static class VolumeNotFoundException extends FallbackException {
        public VolumeNotFoundException(String volumeName) {
            super("Volume " + volumeName + " not found");
        }
    }

    static class VolumeArgumentException extends FallbackException {
        public VolumeArgumentException(File actual, Collection<File> allowed) {
            super("Requested path " + actual + " doesn't appear under " + allowed);
        }
    }

    private @NonNull DatabaseHelper getDatabaseForUri(Uri uri) throws VolumeNotFoundException {
        final String volumeName = resolveVolumeName(uri);
        synchronized (mAttachedVolumeNames) {
            if (!mAttachedVolumeNames.contains(volumeName)) {
                throw new VolumeNotFoundException(volumeName);
            }
        }
        if (MediaStore.VOLUME_INTERNAL.equals(volumeName)) {
            return mInternalDatabase;
        } else {
            return mExternalDatabase;
        }
    }

    static boolean isMediaDatabaseName(String name) {
        if (INTERNAL_DATABASE_NAME.equals(name)) {
            return true;
        }
        if (EXTERNAL_DATABASE_NAME.equals(name)) {
            return true;
        }
        if (name.startsWith("external-") && name.endsWith(".db")) {
            return true;
        }
        return false;
    }

    static boolean isInternalMediaDatabaseName(String name) {
        if (INTERNAL_DATABASE_NAME.equals(name)) {
            return true;
        }
        return false;
    }

    private void attachVolume(Uri uri) {
        attachVolume(MediaStore.getVolumeName(uri));
    }

    public Uri attachVolume(String volume) {
        if (mCallingIdentity.get().pid != android.os.Process.myPid()) {
            throw new SecurityException(
                    "Opening and closing databases not allowed.");
        }

        // Quick sanity check for shady volume names
        MediaStore.checkArgumentVolumeName(volume);

        // Quick sanity check that volume actually exists
        if (!MediaStore.VOLUME_INTERNAL.equals(volume)) {
            try {
                getVolumePath(volume);
            } catch (IOException e) {
                throw new IllegalArgumentException(
                        "Volume " + volume + " currently unavailable", e);
            }
        }

        synchronized (mAttachedVolumeNames) {
            mAttachedVolumeNames.add(volume);
        }

        final Uri uri = MediaStore.AUTHORITY_URI.buildUpon().appendPath(volume).build();
        getContext().getContentResolver().notifyChange(uri, null);
        if (LOCAL_LOGV) Log.v(TAG, "Attached volume: " + volume);
        if (!MediaStore.VOLUME_INTERNAL.equals(volume)) {
            final DatabaseHelper helper = mInternalDatabase;
            ensureDefaultFolders(volume, helper, helper.getWritableDatabase());
        }
        return uri;
    }

    private void detachVolume(Uri uri) {
        detachVolume(MediaStore.getVolumeName(uri));
    }

    public void detachVolume(String volume) {
        if (mCallingIdentity.get().pid != android.os.Process.myPid()) {
            throw new SecurityException(
                    "Opening and closing databases not allowed.");
        }

        // Quick sanity check for shady volume names
        MediaStore.checkArgumentVolumeName(volume);

        if (MediaStore.VOLUME_INTERNAL.equals(volume)) {
            throw new UnsupportedOperationException(
                    "Deleting the internal volume is not allowed");
        }

        // Signal any scanning to shut down
        MediaScanner.instance(getContext()).onDetachVolume(volume);

        synchronized (mAttachedVolumeNames) {
            mAttachedVolumeNames.remove(volume);
        }

        final Uri uri = MediaStore.AUTHORITY_URI.buildUpon().appendPath(volume).build();
        getContext().getContentResolver().notifyChange(uri, null);
        if (LOCAL_LOGV) Log.v(TAG, "Detached volume: " + volume);
    }

    /*
     * Useful commands to enable debugging:
     * $ adb shell setprop log.tag.MediaProvider VERBOSE
     * $ adb shell setprop db.log.slow_query_threshold.`adb shell cat \
     *       /data/system/packages.list |grep "com.android.providers.media " |cut -b 29-33` 0
     * $ adb shell setprop db.log.bindargs 1
     */

    static final String TAG = "MediaProvider";
    static final boolean LOCAL_LOGV = Log.isLoggable(TAG, Log.VERBOSE);

    private static final String INTERNAL_DATABASE_NAME = "internal.db";
    private static final String EXTERNAL_DATABASE_NAME = "external.db";

    // maximum number of cached external databases to keep
    private static final int MAX_EXTERNAL_DATABASES = 3;

    // Delete databases that have not been used in two months
    // 60 days in milliseconds (1000 * 60 * 60 * 24 * 60)
    private static final long OBSOLETE_DATABASE_DB = 5184000000L;

    // Memory optimization - close idle connections after 30s of inactivity
    private static final int IDLE_CONNECTION_TIMEOUT_MS = 30000;

    @GuardedBy("mAttachedVolumeNames")
    private final ArraySet<String> mAttachedVolumeNames = new ArraySet<>();

    private DatabaseHelper mInternalDatabase;
    private DatabaseHelper mExternalDatabase;

    // name of the volume currently being scanned by the media scanner (or null)
    private String mMediaScannerVolume;

    // current FAT volume ID
    private int mVolumeId = -1;

    // WARNING: the values of IMAGES_MEDIA, AUDIO_MEDIA, and VIDEO_MEDIA and AUDIO_PLAYLISTS
    // are stored in the "files" table, so do not renumber them unless you also add
    // a corresponding database upgrade step for it.
    private static final int IMAGES_MEDIA = 1;
    private static final int IMAGES_MEDIA_ID = 2;
    private static final int IMAGES_MEDIA_ID_THUMBNAIL = 3;
    private static final int IMAGES_THUMBNAILS = 4;
    private static final int IMAGES_THUMBNAILS_ID = 5;

    private static final int AUDIO_MEDIA = 100;
    private static final int AUDIO_MEDIA_ID = 101;
    private static final int AUDIO_MEDIA_ID_GENRES = 102;
    private static final int AUDIO_MEDIA_ID_GENRES_ID = 103;
    private static final int AUDIO_MEDIA_ID_PLAYLISTS = 104;
    private static final int AUDIO_MEDIA_ID_PLAYLISTS_ID = 105;
    private static final int AUDIO_GENRES = 106;
    private static final int AUDIO_GENRES_ID = 107;
    private static final int AUDIO_GENRES_ID_MEMBERS = 108;
    private static final int AUDIO_GENRES_ALL_MEMBERS = 109;
    private static final int AUDIO_PLAYLISTS = 110;
    private static final int AUDIO_PLAYLISTS_ID = 111;
    private static final int AUDIO_PLAYLISTS_ID_MEMBERS = 112;
    private static final int AUDIO_PLAYLISTS_ID_MEMBERS_ID = 113;
    private static final int AUDIO_ARTISTS = 114;
    private static final int AUDIO_ARTISTS_ID = 115;
    private static final int AUDIO_ALBUMS = 116;
    private static final int AUDIO_ALBUMS_ID = 117;
    private static final int AUDIO_ARTISTS_ID_ALBUMS = 118;
    private static final int AUDIO_ALBUMART = 119;
    private static final int AUDIO_ALBUMART_ID = 120;
    private static final int AUDIO_ALBUMART_FILE_ID = 121;

    private static final int VIDEO_MEDIA = 200;
    private static final int VIDEO_MEDIA_ID = 201;
    private static final int VIDEO_MEDIA_ID_THUMBNAIL = 202;
    private static final int VIDEO_THUMBNAILS = 203;
    private static final int VIDEO_THUMBNAILS_ID = 204;

    private static final int VOLUMES = 300;
    private static final int VOLUMES_ID = 301;

    private static final int MEDIA_SCANNER = 500;

    private static final int FS_ID = 600;
    private static final int VERSION = 601;

    private static final int FILES = 700;
    private static final int FILES_ID = 701;

    // Used only by the MTP implementation
    private static final int MTP_OBJECTS = 702;
    private static final int MTP_OBJECTS_ID = 703;
    private static final int MTP_OBJECT_REFERENCES = 704;

    // Used only to invoke special logic for directories
    private static final int FILES_DIRECTORY = 706;

    private static final int DOWNLOADS = 800;
    private static final int DOWNLOADS_ID = 801;

    private static final UriMatcher HIDDEN_URI_MATCHER =
            new UriMatcher(UriMatcher.NO_MATCH);

    private static final UriMatcher PUBLIC_URI_MATCHER =
            new UriMatcher(UriMatcher.NO_MATCH);

    private static final String[] PATH_PROJECTION = new String[] {
        MediaStore.MediaColumns._ID,
            MediaStore.MediaColumns.DATA,
    };

    private static final String OBJECT_REFERENCES_QUERY =
        "SELECT " + Audio.Playlists.Members.AUDIO_ID + " FROM audio_playlists_map"
        + " WHERE " + Audio.Playlists.Members.PLAYLIST_ID + "=?"
        + " ORDER BY " + Audio.Playlists.Members.PLAY_ORDER;

    private static int matchUri(Uri uri, boolean allowHidden) {
        final int publicMatch = PUBLIC_URI_MATCHER.match(uri);
        if (publicMatch != UriMatcher.NO_MATCH) {
            return publicMatch;
        }

        final int hiddenMatch = HIDDEN_URI_MATCHER.match(uri);
        if (hiddenMatch != UriMatcher.NO_MATCH) {
            // Detect callers asking about hidden behavior by looking closer when
            // the matchers diverge; we only care about apps that are explicitly
            // targeting a specific public API level.
            if (!allowHidden) {
                throw new IllegalStateException("Unknown URL: " + uri + " is hidden API");
            }
            return hiddenMatch;
        }

        return UriMatcher.NO_MATCH;
    }

    static {
        final UriMatcher publicMatcher = PUBLIC_URI_MATCHER;
        final UriMatcher hiddenMatcher = HIDDEN_URI_MATCHER;

        publicMatcher.addURI(AUTHORITY, "*/images/media", IMAGES_MEDIA);
        publicMatcher.addURI(AUTHORITY, "*/images/media/#", IMAGES_MEDIA_ID);
        publicMatcher.addURI(AUTHORITY, "*/images/media/#/thumbnail", IMAGES_MEDIA_ID_THUMBNAIL);
        publicMatcher.addURI(AUTHORITY, "*/images/thumbnails", IMAGES_THUMBNAILS);
        publicMatcher.addURI(AUTHORITY, "*/images/thumbnails/#", IMAGES_THUMBNAILS_ID);

        publicMatcher.addURI(AUTHORITY, "*/audio/media", AUDIO_MEDIA);
        publicMatcher.addURI(AUTHORITY, "*/audio/media/#", AUDIO_MEDIA_ID);
        publicMatcher.addURI(AUTHORITY, "*/audio/media/#/genres", AUDIO_MEDIA_ID_GENRES);
        publicMatcher.addURI(AUTHORITY, "*/audio/media/#/genres/#", AUDIO_MEDIA_ID_GENRES_ID);
        hiddenMatcher.addURI(AUTHORITY, "*/audio/media/#/playlists", AUDIO_MEDIA_ID_PLAYLISTS);
        hiddenMatcher.addURI(AUTHORITY, "*/audio/media/#/playlists/#", AUDIO_MEDIA_ID_PLAYLISTS_ID);
        publicMatcher.addURI(AUTHORITY, "*/audio/genres", AUDIO_GENRES);
        publicMatcher.addURI(AUTHORITY, "*/audio/genres/#", AUDIO_GENRES_ID);
        publicMatcher.addURI(AUTHORITY, "*/audio/genres/#/members", AUDIO_GENRES_ID_MEMBERS);
        // TODO: not actually defined in API, but CTS tested
        publicMatcher.addURI(AUTHORITY, "*/audio/genres/all/members", AUDIO_GENRES_ALL_MEMBERS);
        publicMatcher.addURI(AUTHORITY, "*/audio/playlists", AUDIO_PLAYLISTS);
        publicMatcher.addURI(AUTHORITY, "*/audio/playlists/#", AUDIO_PLAYLISTS_ID);
        publicMatcher.addURI(AUTHORITY, "*/audio/playlists/#/members", AUDIO_PLAYLISTS_ID_MEMBERS);
        publicMatcher.addURI(AUTHORITY, "*/audio/playlists/#/members/#", AUDIO_PLAYLISTS_ID_MEMBERS_ID);
        publicMatcher.addURI(AUTHORITY, "*/audio/artists", AUDIO_ARTISTS);
        publicMatcher.addURI(AUTHORITY, "*/audio/artists/#", AUDIO_ARTISTS_ID);
        publicMatcher.addURI(AUTHORITY, "*/audio/artists/#/albums", AUDIO_ARTISTS_ID_ALBUMS);
        publicMatcher.addURI(AUTHORITY, "*/audio/albums", AUDIO_ALBUMS);
        publicMatcher.addURI(AUTHORITY, "*/audio/albums/#", AUDIO_ALBUMS_ID);
        // TODO: not actually defined in API, but CTS tested
        publicMatcher.addURI(AUTHORITY, "*/audio/albumart", AUDIO_ALBUMART);
        // TODO: not actually defined in API, but CTS tested
        publicMatcher.addURI(AUTHORITY, "*/audio/albumart/#", AUDIO_ALBUMART_ID);
        // TODO: not actually defined in API, but CTS tested
        publicMatcher.addURI(AUTHORITY, "*/audio/media/#/albumart", AUDIO_ALBUMART_FILE_ID);

        publicMatcher.addURI(AUTHORITY, "*/video/media", VIDEO_MEDIA);
        publicMatcher.addURI(AUTHORITY, "*/video/media/#", VIDEO_MEDIA_ID);
        publicMatcher.addURI(AUTHORITY, "*/video/media/#/thumbnail", VIDEO_MEDIA_ID_THUMBNAIL);
        publicMatcher.addURI(AUTHORITY, "*/video/thumbnails", VIDEO_THUMBNAILS);
        publicMatcher.addURI(AUTHORITY, "*/video/thumbnails/#", VIDEO_THUMBNAILS_ID);

        publicMatcher.addURI(AUTHORITY, "*/media_scanner", MEDIA_SCANNER);

        // NOTE: technically hidden, since Uri is never exposed
        publicMatcher.addURI(AUTHORITY, "*/fs_id", FS_ID);
        // NOTE: technically hidden, since Uri is never exposed
        publicMatcher.addURI(AUTHORITY, "*/version", VERSION);

        hiddenMatcher.addURI(AUTHORITY, "*", VOLUMES_ID);
        hiddenMatcher.addURI(AUTHORITY, null, VOLUMES);

        // Used by MTP implementation
        publicMatcher.addURI(AUTHORITY, "*/file", FILES);
        publicMatcher.addURI(AUTHORITY, "*/file/#", FILES_ID);
        hiddenMatcher.addURI(AUTHORITY, "*/object", MTP_OBJECTS);
        hiddenMatcher.addURI(AUTHORITY, "*/object/#", MTP_OBJECTS_ID);
        hiddenMatcher.addURI(AUTHORITY, "*/object/#/references", MTP_OBJECT_REFERENCES);

        // Used only to trigger special logic for directories
        hiddenMatcher.addURI(AUTHORITY, "*/dir", FILES_DIRECTORY);

        publicMatcher.addURI(AUTHORITY, "*/downloads", DOWNLOADS);
        publicMatcher.addURI(AUTHORITY, "*/downloads/#", DOWNLOADS_ID);
    }

    /**
     * Set of columns that can be safely mutated by external callers; all other
     * columns are treated as read-only, since they reflect what the media
     * scanner found on disk, and any mutations would be overwritten the next
     * time the media was scanned.
     */
    private static final ArraySet<String> sMutableColumns = new ArraySet<>();

    {
        sMutableColumns.add(MediaStore.MediaColumns.DATA);
        sMutableColumns.add(MediaStore.MediaColumns.RELATIVE_PATH);
        sMutableColumns.add(MediaStore.MediaColumns.DISPLAY_NAME);
        sMutableColumns.add(MediaStore.MediaColumns.IS_PENDING);
        sMutableColumns.add(MediaStore.MediaColumns.IS_TRASHED);
        sMutableColumns.add(MediaStore.MediaColumns.DATE_EXPIRES);
        sMutableColumns.add(MediaStore.MediaColumns.PRIMARY_DIRECTORY);
        sMutableColumns.add(MediaStore.MediaColumns.SECONDARY_DIRECTORY);

        sMutableColumns.add(MediaStore.Audio.AudioColumns.BOOKMARK);

        sMutableColumns.add(MediaStore.Video.VideoColumns.TAGS);
        sMutableColumns.add(MediaStore.Video.VideoColumns.CATEGORY);
        sMutableColumns.add(MediaStore.Video.VideoColumns.BOOKMARK);

        sMutableColumns.add(MediaStore.Audio.Playlists.NAME);
        sMutableColumns.add(MediaStore.Audio.Playlists.Members.AUDIO_ID);
        sMutableColumns.add(MediaStore.Audio.Playlists.Members.PLAY_ORDER);

        sMutableColumns.add(MediaStore.Files.FileColumns.MIME_TYPE);
        sMutableColumns.add(MediaStore.Files.FileColumns.MEDIA_TYPE);
    }

    /**
     * Set of columns that affect placement of files on disk.
     */
    private static final ArraySet<String> sPlacementColumns = new ArraySet<>();

    {
        sPlacementColumns.add(MediaStore.MediaColumns.DATA);
        sPlacementColumns.add(MediaStore.MediaColumns.RELATIVE_PATH);
        sPlacementColumns.add(MediaStore.MediaColumns.DISPLAY_NAME);
        sPlacementColumns.add(MediaStore.MediaColumns.MIME_TYPE);
        sPlacementColumns.add(MediaStore.MediaColumns.PRIMARY_DIRECTORY);
        sPlacementColumns.add(MediaStore.MediaColumns.SECONDARY_DIRECTORY);
    }

    /**
     * List of abusive custom columns that we're willing to allow via
     * {@link SQLiteQueryBuilder#setProjectionGreylist(List)}.
     */
    static final ArrayList<Pattern> sGreylist = new ArrayList<>();

    private static void addGreylistPattern(String pattern) {
        sGreylist.add(Pattern.compile(" *" + pattern + " *"));
    }

    static {
        final String maybeAs = "( (as )?[_a-z0-9]+)?";
        addGreylistPattern("(?i)[_a-z0-9]+" + maybeAs);
        addGreylistPattern("audio\\._id AS _id");
        addGreylistPattern("(?i)(min|max|sum|avg|total|count|cast)\\(([_a-z0-9]+" + maybeAs + "|\\*)\\)" + maybeAs);
        addGreylistPattern("case when case when \\(date_added >= \\d+ and date_added < \\d+\\) then date_added \\* \\d+ when \\(date_added >= \\d+ and date_added < \\d+\\) then date_added when \\(date_added >= \\d+ and date_added < \\d+\\) then date_added / \\d+ else \\d+ end > case when \\(date_modified >= \\d+ and date_modified < \\d+\\) then date_modified \\* \\d+ when \\(date_modified >= \\d+ and date_modified < \\d+\\) then date_modified when \\(date_modified >= \\d+ and date_modified < \\d+\\) then date_modified / \\d+ else \\d+ end then case when \\(date_added >= \\d+ and date_added < \\d+\\) then date_added \\* \\d+ when \\(date_added >= \\d+ and date_added < \\d+\\) then date_added when \\(date_added >= \\d+ and date_added < \\d+\\) then date_added / \\d+ else \\d+ end else case when \\(date_modified >= \\d+ and date_modified < \\d+\\) then date_modified \\* \\d+ when \\(date_modified >= \\d+ and date_modified < \\d+\\) then date_modified when \\(date_modified >= \\d+ and date_modified < \\d+\\) then date_modified / \\d+ else \\d+ end end as corrected_added_modified");
        addGreylistPattern("MAX\\(case when \\(datetaken >= \\d+ and datetaken < \\d+\\) then datetaken \\* \\d+ when \\(datetaken >= \\d+ and datetaken < \\d+\\) then datetaken when \\(datetaken >= \\d+ and datetaken < \\d+\\) then datetaken / \\d+ else \\d+ end\\)");
        addGreylistPattern("MAX\\(case when \\(date_added >= \\d+ and date_added < \\d+\\) then date_added \\* \\d+ when \\(date_added >= \\d+ and date_added < \\d+\\) then date_added when \\(date_added >= \\d+ and date_added < \\d+\\) then date_added / \\d+ else \\d+ end\\)");
        addGreylistPattern("MAX\\(case when \\(date_modified >= \\d+ and date_modified < \\d+\\) then date_modified \\* \\d+ when \\(date_modified >= \\d+ and date_modified < \\d+\\) then date_modified when \\(date_modified >= \\d+ and date_modified < \\d+\\) then date_modified / \\d+ else \\d+ end\\)");
        addGreylistPattern("\"content://media/[a-z]+/audio/media\"");
        addGreylistPattern("substr\\(_data, length\\(_data\\)-length\\(_display_name\\), 1\\) as filename_prevchar");
        addGreylistPattern("\\*" + maybeAs);
        addGreylistPattern("case when \\(datetaken >= \\d+ and datetaken < \\d+\\) then datetaken \\* \\d+ when \\(datetaken >= \\d+ and datetaken < \\d+\\) then datetaken when \\(datetaken >= \\d+ and datetaken < \\d+\\) then datetaken / \\d+ else \\d+ end");
    }

    @GuardedBy("sProjectionMapCache")
    private static final ArrayMap<Class<?>, ArrayMap<String, String>>
            sProjectionMapCache = new ArrayMap<>();

    /**
     * Return a projection map that represents the valid columns that can be
     * queried the given contract class. The mapping is built automatically
     * using the {@link Column} annotation, and is designed to ensure that we
     * always support public API commitments.
     */
    static ArrayMap<String, String> getProjectionMap(Class<?> clazz) {
        synchronized (sProjectionMapCache) {
            ArrayMap<String, String> map = sProjectionMapCache.get(clazz);
            if (map == null) {
                map = new ArrayMap<>();
                sProjectionMapCache.put(clazz, map);
                try {
                    for (Field field : clazz.getFields()) {
                        if (field.isAnnotationPresent(Column.class)) {
                            final String column = (String) field.get(null);
                            map.put(column, column);
                        }
                    }
                } catch (ReflectiveOperationException e) {
                    throw new RuntimeException(e);
                }
            }
            return map;
        }
    }

    /**
     * Simple attempt to balance the given SQL expression by adding parenthesis
     * when needed.
     * <p>
     * Since this is only used for recovering from abusive apps, we're not
     * interested in trying to build a fully valid SQL parser up in Java. It'll
     * give up when it encounters complex SQL, such as string literals.
     */
    @VisibleForTesting
    static @Nullable String maybeBalance(@Nullable String sql) {
        if (sql == null) return null;

        int count = 0;
        char literal = '\0';
        for (int i = 0; i < sql.length(); i++) {
            final char c = sql.charAt(i);

            if (c == '\'' || c == '"') {
                if (literal == '\0') {
                    // Start literal
                    literal = c;
                } else if (literal == c) {
                    // End literal
                    literal = '\0';
                }
            }

            if (literal == '\0') {
                if (c == '(') {
                    count++;
                } else if (c == ')') {
                    count--;
                }
            }
        }
        while (count > 0) {
            sql = sql + ")";
            count--;
        }
        while (count < 0) {
            sql = "(" + sql;
            count++;
        }
        return sql;
    }

    static <T> boolean containsAny(Set<T> a, Set<T> b) {
        for (T i : b) {
            if (a.contains(i)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Gracefully recover from abusive callers that are smashing invalid
     * {@code GROUP BY} clauses into {@code WHERE} clauses.
     */
    @VisibleForTesting
    static Pair<String, String> recoverAbusiveGroupBy(Pair<String, String> selectionAndGroupBy) {
        final String origSelection = selectionAndGroupBy.first;
        final String origGroupBy = selectionAndGroupBy.second;

        final int index = (origSelection != null)
                ? origSelection.toUpperCase().indexOf(" GROUP BY ") : -1;
        if (index != -1) {
            String selection = origSelection.substring(0, index);
            String groupBy = origSelection.substring(index + " GROUP BY ".length());

            // Try balancing things out
            selection = maybeBalance(selection);
            groupBy = maybeBalance(groupBy);

            // Yell if we already had a group by requested
            if (!TextUtils.isEmpty(origGroupBy)) {
                throw new IllegalArgumentException(
                        "Abusive '" + groupBy + "' conflicts with requested '" + origGroupBy + "'");
            }

            Log.w(TAG, "Recovered abusive '" + selection + "' and '" + groupBy + "' from '"
                    + origSelection + "'");
            return Pair.create(selection, groupBy);
        } else {
            return selectionAndGroupBy;
        }
    }

    @VisibleForTesting
    static @Nullable Uri computeCommonPrefix(@NonNull List<Uri> uris) {
        if (uris.isEmpty()) return null;

        final Uri base = uris.get(0);
        final List<String> basePath = new ArrayList<>(base.getPathSegments());
        for (int i = 1; i < uris.size(); i++) {
            final List<String> probePath = uris.get(i).getPathSegments();
            for (int j = 0; j < basePath.size() && j < probePath.size(); j++) {
                if (!Objects.equals(basePath.get(j), probePath.get(j))) {
                    // Trim away all remaining common elements
                    while (basePath.size() > j) {
                        basePath.remove(j);
                    }
                }
            }

            final int probeSize = probePath.size();
            while (basePath.size() > probeSize) {
                basePath.remove(probeSize);
            }
        }

        final Uri.Builder builder = base.buildUpon().path(null);
        for (int i = 0; i < basePath.size(); i++) {
            builder.appendPath(basePath.get(i));
        }
        return builder.build();
    }

    @Deprecated
    private String getCallingPackageOrSelf() {
        return mCallingIdentity.get().getPackageName();
    }

    @Deprecated
    private int getCallingPackageTargetSdkVersion() {
        return mCallingIdentity.get().getTargetSdkVersion();
    }

    @Deprecated
    private boolean isCallingPackageAllowedHidden() {
        return isCallingPackageSystem();
    }

    @Deprecated
    private boolean isCallingPackageSystem() {
        return mCallingIdentity.get().hasPermission(PERMISSION_IS_SYSTEM);
    }

    @Deprecated
    private boolean isCallingPackageLegacy() {
        return mCallingIdentity.get().hasPermission(PERMISSION_IS_LEGACY);
    }

    @Override
    public void dump(FileDescriptor fd, PrintWriter writer, String[] args) {
        final IndentingPrintWriter pw = new IndentingPrintWriter(writer, "  ");
        pw.printPair("mThumbSize", mThumbSize);
        pw.println();
        pw.printPair("mAttachedVolumeNames", mAttachedVolumeNames);
        pw.println();

        pw.println(dump(mInternalDatabase, true));
        pw.println(dump(mExternalDatabase, true));
    }

    private String dump(DatabaseHelper dbh, boolean dumpDbLog) {
        StringBuilder s = new StringBuilder();
        s.append(dbh.mName);
        s.append(": ");
        SQLiteDatabase db = dbh.getReadableDatabase();
        if (db == null) {
            s.append("null");
        } else {
            s.append("version " + db.getVersion() + ", ");
            Cursor c = db.query("files", new String[] {"count(*)"}, null, null, null, null, null);
            try {
                if (c != null && c.moveToFirst()) {
                    int num = c.getInt(0);
                    s.append(num + " rows, ");
                } else {
                    s.append("couldn't get row count, ");
                }
            } finally {
                IoUtils.closeQuietly(c);
            }
            if (dbh.mScanStartTime != 0) {
                s.append("scan started " + DateUtils.formatDateTime(getContext(),
                        dbh.mScanStartTime / 1000,
                        DateUtils.FORMAT_SHOW_DATE
                        | DateUtils.FORMAT_SHOW_TIME
                        | DateUtils.FORMAT_ABBREV_ALL));
                long now = dbh.mScanStopTime;
                if (now < dbh.mScanStartTime) {
                    now = SystemClock.currentTimeMicro();
                }
                s.append(" (" + DateUtils.formatElapsedTime(
                        (now - dbh.mScanStartTime) / 1000000) + ")");
                if (dbh.mScanStopTime < dbh.mScanStartTime) {
                    if (mMediaScannerVolume != null &&
                            dbh.mName.startsWith(mMediaScannerVolume)) {
                        s.append(" (ongoing)");
                    } else {
                        s.append(" (scanning " + mMediaScannerVolume + ")");
                    }
                }
            }
            if (dumpDbLog) {
                c = db.query("log", new String[] {"time", "message"},
                        null, null, null, null, "rowid");
                try {
                    if (c != null) {
                        while (c.moveToNext()) {
                            String when = c.getString(0);
                            String msg = c.getString(1);
                            s.append("\n" + when + " : " + msg);
                        }
                    }
                } finally {
                    IoUtils.closeQuietly(c);
                }
            } else {
                s.append(": pid=" + android.os.Process.myPid());
                s.append(", fingerprint=" + Build.FINGERPRINT);
            }
        }
        return s.toString();
    }

    /**
     * Returns the canonical {@link File} for the provided abstract pathname.
     *
     * @return The canonical pathname string denoting the same file or directory as this abstract
     *         pathname
     * @see File#getCanonicalFile()
     */
    @NonNull
    public static File getCanonicalFile(@NonNull String path) throws IOException {
        Objects.requireNonNull(path);
        return new File(path).getCanonicalFile();
    }

    /**
     * Returns the canonical pathname string of the provided abstract pathname.
     *
     * @return The canonical pathname string denoting the same file or directory as this abstract
     *         pathname.
     * @see File#getCanonicalPath()
     */
    @NonNull
    public static String getCanonicalPath(@NonNull String path) throws IOException {
        Objects.requireNonNull(path);
        return new File(path).getCanonicalPath();
    }

}
